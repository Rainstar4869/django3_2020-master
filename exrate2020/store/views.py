from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
import logging
import json
from .forms import CheckoutForm
from .models import ShippingAddress
from .serializers import OrderSerializer, ItemSerializer

from .models import (
    Item,
    Order,
    OrderItem
)

CATEGORY = (
    ('S', 'Shirt'),
    ('SP', 'Sport Wear'),
    ('OW', 'Out Wear')
)

logger = logging.getLogger("error")


# Create your views here.
class HomeView(ListView):
    model = Item
    template_name = "shop/home.html"
    context_object_name = "products"

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["categories"] = CATEGORY
        return context


class ProductView(DetailView):
    model = Item
    template_name = "shop/product.html"


class OrderSummaryView(LoginRequiredMixin, View):
    login_url = "/webauth/login/"

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order': order
            }
            logger.error(context)
            return render(self.request, 'shop/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("/")


class CheckoutView(LoginRequiredMixin, View):
    login_url = "/webauth/login/"

    def get(self, *args, **kwargs):
        try:
            form = CheckoutForm()

            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                "order": order,
                "form": form
            }
            return render(self.request, "shop/checkout.html", context)

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("/")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                logger.error(" form is_valid")
                logger.error(str(form.cleaned_data))
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                phone = form.cleaned_data.get('phone')
                postcode = form.cleaned_data.get('postcode')
                state = form.cleaned_data.get('state')
                town = form.cleaned_data.get('town')
                street = form.cleaned_data.get('street')
                address_1 = form.cleaned_data.get('address_1')
                address_2 = form.cleaned_data.get('address_2')

                checkout_address = ShippingAddress(
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
                order.checkout_address = checkout_address
                # order.ordered = True
                order.save()

                # order.items.update(ordered=True)

                messages.success(self.request, "Place Order successfully!")
                return redirect('store:checkout')

            messages.warning(self.request, "Failed Chekout")
            return redirect('store:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("store:order-summary")


@login_required(login_url="/webauth/login/")
def add_to_cart(request, pk, location):
    item = get_object_or_404(Item, pk=pk)
    logger.error(location)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added quantity Item")
            return redirect(location)
            # return redirect("store:order-summary")
        else:
            order.items.add(order_item)
            return redirect(location)
            # return redirect("store:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        # messages.info(request, "Item added to your cart")
        return redirect(location)
        # return redirect("store:order-summary")


@login_required(login_url="/webauth/login/")
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            messages.info(request, "Item \"" + order_item.item.item_name + "\" remove from your cart")
            return redirect("store:order-summary")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("store:product", pk=pk)
    else:
        # add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("store:product", pk=pk)


@login_required(login_url="/webauth/login/")
def reduce_quantity_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            # messages.info(request, "Item quantity was updated")
            return redirect("store:order-summary")
        else:
            # messages.info(request, "This Item not in your cart")
            return redirect("store:order-summary")
    else:
        # add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("store:order-summary")


class ProductAPIView(View):
    def post(self, request):
        data = json.loads(request.body)
        pk = data["product_id"]

        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(instance=item, many=False)

        return JsonResponse({
            "result": "OK",
            "product": serializer.data,
        })


class AddToChartAPIView(View):
    def post(self, request):
        data = json.loads(request.body)
        pk = data["product_id"]
        user = request.user

        logger.error(request.path)
        item = get_object_or_404(Item, pk=pk)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]

            if order.items.filter(item__pk=item.pk).exists():
                order_item.quantity += 1
                order_item.save()
            else:
                order.items.add(order_item)

        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)

        serializer = OrderSerializer(instance=order, many=False)

        return JsonResponse({
            "result": "OK",
            "product_id": data["product_id"],
            "order_count": order.get_total_quantity(),
            "order": serializer.data
        })
