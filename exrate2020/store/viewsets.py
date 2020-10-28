from django.forms import model_to_dict
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ShippingAddressSerializer, OrderSerializer, MarginSerializer, ItemSerializer
from .models import ShippingAddress, Order, OrderItem, Margin, Item, Category
from .cart import Cart as _Cart
from authentication.models import User
import logging
from rest_framework import status
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.exceptions import ObjectDoesNotExist
import json
from django.conf import settings

logger = logging.getLevelName("error_logger")
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class ShippingAddressViewSet(GenericViewSet):
    serializer_class = ShippingAddressSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request, *args, **kwargs):
        addressbook = ShippingAddress.objects.filter(user=self.request.user)
        if addressbook.exists():
            addressbook_serializer = self.serializer_class(instance=addressbook, many=True)
            return Response({
                "result": "OK",
                "operation": "list",
                "addressbook": addressbook_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "result": "NG",
            "operation": "list",
            "addressbook": []
        }, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            address = ShippingAddress.objects.get(pk=pk, user=self.request.user)
            address.delete()
            return Response({
                "result": "OK",
                "operation": "destroy",
                "message": "successfully deleted!",
                "id": pk
            }, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({
                "result": "NG",
                "operation": "destroy",
                "message": "record doesn't exists!",
                "id": pk
            }, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            address = ShippingAddress.objects.get(pk=pk, user=self.request.user)
            address_serializer = ShippingAddressSerializer(instance=address, many=False)

            return Response({
                "result": "OK",
                "operation": "get address of pk={}".format(pk),
                "message": "successfully retrieved!",
                "address": address_serializer.data
            }, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({
                "result": "NG",
                "operation": "get address of pk={}".format(pk),
                "message": "Retrieved failed!",
                "address": {}
            }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = json.loads(request.body)
        pk = data['id']
        name = data['name']
        email = data['email']
        phone = data['phone']
        postcode = data['postcode']
        state = data['state']
        town = data['town']
        street = data['street']
        address_1 = data['address_1']
        address_2 = data['address_2']

        try:
            address = ShippingAddress.objects.get(pk=pk, user=self.request.user)
            address.name = name
            address.phone = phone
            address.postcode = postcode
            address.email = email
            address.state = state
            address.town = town
            address.street = street
            address.address_1 = address_1
            address.address_2 = address_2

            address.save()

            address_serializer = ShippingAddressSerializer(instance=address, many=False)

            return Response({
                "result": "OK",
                "operation": "get address of pk={}".format(pk),
                "message": "successfully retrieved!",
                "address": address_serializer.data
            }, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({
                "result": "NG",
                "operation": "get address of pk={}".format(pk),
                "message": "Retrieved failed!",
                "address": {}
            }, status=status.HTTP_200_OK)


class OrderViewSet(GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        orders = Order.objects.filter(user=request.user)
        if orders.exists():
            orders_serializer = self.serializer_class(instance=orders, many=True)
            return Response({
                "result": "OK",
                "operation": "list",
                "count": orders.count(),
                "orders": orders_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "result": "NG",
            "operation": "list",
            "count": 0,
            "orders": []
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = request.user
        session_cart = _Cart(request.session, user.id)

        if session_cart:
            order = Order.objects.create(
                user=user,
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
                existed_address_id = data['existed_address_id']
                checkout_address = ShippingAddress.objects.get(pk=existed_address_id)
            except ObjectDoesNotExist:
                name = data['name']
                email = data['email']
                phone = data['phone']
                postcode = data['postcode']
                state = data['state']
                town = data['town']
                street = data['street']
                address_1 = data['address_1']
                address_2 = data['address_2']

                checkout_address = ShippingAddress(
                    user=user,
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
            return Response({
                "result": "OK",
                "operation": "create",
                "request": str(data),
            }, status=status.HTTP_200_OK)

        return Response({
            "result": "OK",
            "operation": "create",
            "request": str(data),
        }, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
            order.delete()
            return Response({
                "result": "OK",
                "operation": "destroy",
                "message": "successfully deleted!",
                "id": pk
            }, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({
                "result": "NG",
                "operation": "destroy",
                "message": "record doesn't exists!",
                "id": pk
            }, status=status.HTTP_200_OK)

    def caculate_margins(self, order):
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
            logger.error("order_{}, distibute to ADMIN with margin {} ".format(order.id, margin_left))
            adminuser = User.objects.get(username=settings.ADMIN_NAME)
            Margin.objects.create(
                order=order,
                user=adminuser,
                level=100,
                amount=margin_left,
            )


class MarginViewSet(GenericViewSet):
    serializer_class = MarginSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        margins = Margin.objects.filter(user=request.user)

        if margins.exists():
            margins_serializer = self.serializer_class(instance=margins, many=True)
            return Response({
                "result": "OK",
                "operation": "list",
                "count": margins.count(),
                "margins": margins_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "result": "NG",
            "operation": "list",
            "count": 0,
            "margins": []
        }, status=status.HTTP_200_OK)


class ProductViewSet(GenericViewSet):
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)

    # @action(detail=False, methods=['post'])
    def list(self, request):

        products = cache.get("nichiei_store_all_products")

        if products is None:
            products = Item.objects.all().defer("buy_price", "discount_price", "distributor_price")
            cache.set("nichiei_store_all_products", products, CACHE_TTL)

        if products.exists():
            product_serializer = ItemSerializer(instance=products, many=True)

            return Response({
                "result": "OK",
                "operation": "list all products",
                "count": products.count(),
                "products": product_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "result": "NG",
            "operation": "list all products",
            "count": 0,
            "products": []
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def list_by_category(self, request):
        data = json.loads(request.body)
        category_id = data["category_id"]

        print("category_id: {}".format(category_id))
        # logger.error("category_id: {}".format(category_id))
        category = Category.objects.get(pk=category_id)
        categories = category.get_descendants(include_self=True)

        products = Item.objects.filter(category__in=categories)

        if products.exists():
            products_serializer = ItemSerializer(instance=products, many=True)

            return Response({
                "result": "OK",
                "operation": "list products by category",
                "count": products.count(),
                "products": products_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "result": "NG",
            "operation": "list products by category",
            "count": 0,
            "products": []
        }, status=status.HTTP_200_OK)
