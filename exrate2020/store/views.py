from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Sum
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
import logging
import json
from weasyprint import HTML, CSS
import tempfile
import datetime
from django.conf import settings
from django.core import serializers
from .forms import CheckoutForm
from .models import Category
from .serializers import OrderSerializer, ItemSerializer, CategorySerializer, ShippingAddressSerializer
from authentication.models import User
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from qr_code.qrcode.utils import ContactDetail
from . import settings as carton_settings
from .cart import Cart as _Cart
from django.forms.models import model_to_dict
from .models import (
    Item,
    Order,
    OrderItem,
    ShippingAddress,
    Margin
)

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
CATEGORY = (
    ('S', 'Shirt'),
    ('SP', 'Sport Wear'),
    ('OW', 'Out Wear')
)

logger = logging.getLogger("error_logger")


@login_required(login_url="/webauth/login/")
def export_pdf_order(request, slug):
    current_site = get_current_site(request)
    register_url = 'http://' + current_site.domain + "/webauth/register/?introcode=" + str(request.user.introcode)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline;attachment;filename=Expenses" + str(datetime.datetime.now()) + '.pdf'
    response["Content-Transfer-Encoding"] = "binary"

    order = Order.objects.get(slug=slug)

    if order.user == request.user:
        html_string = render_to_string("shop/pdfs/invoice_pdf.html", {
            "order": order,
            "json_shippingaddress": json.loads(order.json_shippingaddress)
        })
        result = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
            stylesheets=[
                CSS('staticfiles/css/invoice_pdf.css')
            ])

        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, "rb")
            response.write(output.read())

        return response

    return redirect("store:home")


@method_decorator(login_required(login_url='/webauth/login/'), name="dispatch")
class AddressBookListView(ListView):
    model = Margin
    template_name = "shop/accounts/addressbook.html"
    context_object_name = "addressbook"
    paginate_by = 10

    def get_queryset(self):
        logger.error(self.request.user)
        margins = ShippingAddress.objects.filter(user=self.request.user)
        return margins


class SearchProductView(ListView):
    model = Item
    template_name = "shop/home.html"
    context_object_name = "products"
    searchKey = ""

    def get_queryset(self):
        keyval = self.request.GET.get("q", "")
        self.searchKey = keyval
        products = Item.objects.filter(item_name__icontains=keyval) | \
                   Item.objects.filter(description__icontains=keyval)
        logger.error("get_queryset: search product with keyval {}".format(keyval))
        return products

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        context["keyval"] = self.searchKey

        logger.error("get_context_data: search product with keyval {}".format(self.searchKey))
        return context


# @cache_page(CACHE_TTL)
@method_decorator(login_required(login_url='/webauth/login/'), name="dispatch")
class HomeView(ListView):
    model = Item
    template_name = "shop/home.html"
    context_object_name = "products"

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cart"] = _Cart(self.request, self.request.user.id)
        return context

    def get_queryset(self):
        products = cache.get("nichiei_store_all_products")

        if products is None:
            products = Item.objects.all().defer("buy_price", "discount_price", "distributor_price")
            cache.set("nichiei_store_all_products", products, CACHE_TTL)

        return products


def get_order_from_json(jsonstr):
    modelobject = None
    for obj in serializers.deserialize('json', jsonstr):
        modelobject = obj.object

    return modelobject


@method_decorator(login_required(login_url='/webauth/login/'), name="dispatch")
class OrderListView(ListView):
    model = Order
    template_name = "shop/accounts/orders.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user, ordered=True).select_related("user").prefetch_related(
            "orderitems").order_by("-id")
        return orders


class ProductView(DetailView):
    model = Item
    template_name = "shop/product.html"


class OrderSummaryView(LoginRequiredMixin, View):
    login_url = "/webauth/login/"

    def get(self, *args, **kwargs):
        return render(self.request, 'shop/order_summary.html')


class CheckoutView(LoginRequiredMixin, View):
    login_url = "/webauth/login/"

    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            "form": form
        }
        return render(self.request, "shop/checkout.html", context)

    def post(self, *args, **kwargs):
        session_cart = _Cart(self.request.session, self.request.user.id)

        if session_cart:
            order = Order.objects.create(
                user=self.request.user,
                json_orderitems=session_cart.cart_serializable,
                Qty=session_cart.count,
                Total=session_cart.total
            )

            for item in session_cart.items:
                final_price = item.product.discount_price if item.product.discount_price < item.product.price else item.product.price
                final_subtotal = final_price * item.quantity
                OrderItem.objects.create(
                    order=order,
                    item=item.product,
                    quantity=item.quantity,
                    final_subtotal=final_subtotal,
                    final_price=final_price)

            try:
                existed_address_id = self.request.POST.get('existed_address_id', 0)
                checkout_address = ShippingAddress.objects.get(pk=existed_address_id)
            except ObjectDoesNotExist:
                name = self.request.POST.get('name')
                email = self.request.POST.get('email')
                phone = self.request.POST.get('phone')
                postcode = self.request.POST.get('postcode')
                state = self.request.POST.get('state')
                town = self.request.POST.get('town')
                street = self.request.POST.get('street')
                address_1 = self.request.POST.get('address_1')
                address_2 = self.request.POST.get('address_2')

                checkout_address = ShippingAddress(
                    user=self.request.user,
                    name=name,
                    email=email,
                    phone=phone,
                    postcode=postcode,
                    state=state,
                    town=town,
                    street=street,
                    address_1=address_1,
                    address_2=address_2,
                )

            checkout_address.save()

            order.shippingaddress = checkout_address
            order.json_shippingaddress = model_to_dict(checkout_address)
            order.ordered = True
            order.save(update_fields=["ordered", "shippingaddress", "json_shippingaddress"])

            self.caculate_margins(order)
            session_cart.clear()

            messages.success(self.request, "Place Order successfully!")
            return render(self.request, "shop/checkout_completed.html", {"order": order})
        else:
            messages.error(self.request, "You do not have an order")
            return redirect("store:checkout")

    def caculate_margins(self, order):
        if order:
            last_index = len(settings.MARGIN_RATES)
            user_profile = order.user.profile
            ancestors = user_profile.get_ancestors(ascending=True, include_self=False)
            ancestors_list = list(ancestors)

            if len(ancestors_list) >= 1:
                ancestors_list.pop()  # remove last root element

            margin_left = order.get_total_distributor_margin()

            if ancestors_list:
                margin_left_loop = margin_left
                logger.error("margin_left {} ".format(margin_left))

                for level in range(len(ancestors_list[:last_index])):
                    level_rate = settings.MARGIN_RATES[str(level + 1)]
                    level_margin = int(margin_left_loop * level_rate)
                    user = ancestors_list[level].user

                    if user.orders.count() >= settings.MARGIN_CRITERIA_ORDERS:
                        Margin.objects.create(
                            order=order,
                            user=user,
                            level=level,
                            amount=level_margin,
                        )
                        margin_left -= level_margin

            if margin_left:
                # mount left margin to root

                logger.error("order_{}, distibute to ADMIN with margin {} ".format(order.id, margin_left))
                adminuser = User.objects.get(username=settings.ADMIN_NAME)
                Margin.objects.create(
                    order=order,
                    user=adminuser,
                    level=100,
                    amount=margin_left,
                )


@method_decorator(login_required(login_url='/webauth/login/'), name="dispatch")
class MarginListView(ListView):
    model = Margin
    template_name = "shop/accounts/margins.html"
    context_object_name = "margins"
    paginate_by = 10

    def get_queryset(self):
        query_kwards = settings.VALID_USER_MARGIN_LOOKUP
        margins = Margin.objects.filter(user=self.request.user, **query_kwards).select_related("order")
        return margins

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(MarginListView, self).get_context_data(*args, **kwargs)
        margin_summary = Margin.objects.filter(is_valid=True).aggregate(total_amount=Sum("amount"),
                                                                        total_count=Count("id"))
        context["margin_summary"] = margin_summary
        return context


@login_required(login_url="/webauth/login/")
def show_dashboard(request):
    current_site = get_current_site(request)
    register_url = 'http://' + current_site.domain + "/webauth/register/?introcode=" + str(request.user.introcode)

    contact_detail = ContactDetail(
        first_name=request.user.username,
        email=request.user.email,
        url=register_url
    )

    context = {
        "qrcode_introcode": contact_detail.url,
        "membertree": request.user.profile.get_descendants(include_self=True)
    }
    return render(request, "shop/accounts/dashboard.html", context)


class ProductAPIView(View):
    def post(self, request):
        # data = json.loads(request.body)
        pk = request.POST.get("product_id")
        cat_first = Category.objects.filter(parent=None)
        cat_serializer = CategorySerializer(instance=cat_first, many=True)

        logger.error("ProductAPIView pk: ".format(pk))

        if pk:
            item = get_object_or_404(Item, pk=pk)
            serializer = ItemSerializer(instance=item, many=False)
        else:
            # first_category = Category.objects.first()
            # logger.error("first_category: ")
            # logger.error(first_category)
            # items = Item.objects.filter(category=first_category)
            items = Item.objects.all()
            # logger.error("items: ")
            # logger.error(items)
            serializer = ItemSerializer(instance=items, many=True)

        return JsonResponse({
            "result": "OK",
            "function": "ProductAPIView post",
            "products": serializer.data,
            "cats": cat_serializer.data
        })


class CategoryAPIView(View):
    def post(self, request):
        cats = Category.objects.filter(parent=None)

        if cats.exists():
            cat_serializer = CategorySerializer(instance=cats, many=True)

            return JsonResponse({
                "result": "OK",
                "categories": cat_serializer.data
            })
        else:
            return JsonResponse({
                "result": "NG",
                "categories": []
            })


# class CategoryProductAPIView(View):
#     def post(self, request):
#
#         data = json.loads(request.body)
#         category_id = data["category_id"]
#         category = Category.objects.get(pk=category_id)
#         categories = category.get_descendants(include_self=True)
#
#         products = Item.objects.filter(category__in=categories)
#
#         if products.exists():
#             products_serializer = ItemSerializer(instance=products, many=True)
#
#             return JsonResponse({
#                 "result": "OK",
#                 "category_products": products_serializer.data
#             })
#         else:
#             return JsonResponse({
#                 "result": "NG",
#                 "category_products": []
#             })


class ShippingAddressAPIView(View):
    def get(self, request):

        shippingaddress = ShippingAddress.objects.filter(user=request.user)

        if shippingaddress.exists():
            shippingaddress_serializer = ShippingAddressSerializer(instance=shippingaddress, many=True)

            return JsonResponse({
                "result": "OK",
                "shippingaddress": shippingaddress_serializer.data
            })
        else:
            return JsonResponse({
                "result": "NG",
                "shippingaddress": []
            })

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        id = data["id"]

        try:
            shippingaddress = ShippingAddress.objects.get(pk=id)
            shippingaddress.delete()
            return JsonResponse({
                "result": "OK",
                "message": "shippingaddress deleted",
                "id": id
            })
        except ObjectDoesNotExist:
            return JsonResponse({
                "result": "OK",
                "message": "shippingaddress doesn't exist",
                "id": id
            })


class ShoppingCartOperation(View):
    def get(self, request):
        cart = _Cart(request.session, request.user.id)
        return JsonResponse({
            "result": "OK",
            "cart": cart.cart_serializable
        })

    def post(self, request):
        data = json.loads(request.body)
        pk = data["product_id"]
        action = data["action"]
        logger.error("update shopping cart")
        logger.error(pk)
        logger.error(action)

        try:
            cache_product = cache.get("product_{}".format(pk))
            if cache_product is None:
                cache_product = Item.objects.get(pk=pk)
                cache.set("product_{}".format(pk), cache_product, settings.CACHE_TTL)

            cart = _Cart(request.session, request.user.id)

            if action == "remove_cartitem":
                cart.remove(cache_product)
            if action == "add_cartitem":
                cart.add(cache_product, price=cache_product.price)
            elif action == "decrease_cartitem":
                cart.remove_single(cache_product)

            return JsonResponse({
                "result": "OK",
                "type": action,
                "cart": cart.cart_serializable
            })
        except ObjectDoesNotExist:
            return JsonResponse({
                "result": "NG",
                "cart": {}
            })
