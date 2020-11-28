from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .viewsets import ShippingAddressViewSet, OrderViewSet, \
    MarginViewSet, ProductViewSet, PingoOrderViewSet, PingoItemViewSet, NewProductViewSet

from .views import (
    ProductView,
    SearchProductView,
    HomeView,
    OrderSummaryView,
    CheckoutView,
    Pingo_Checkout,
    ShoppingCartOperation,
    ShippingAddressAPIView,
    ProductAPIView,
    OrderListView,
    MarginListView,
    AddressBookListView,

    CategoryAPIView,
    # CategoryProductAPIView,

    show_dashboard,
    export_pdf_order,
)

app_name = 'store'
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

router = DefaultRouter()
router.register("shippingadress", ShippingAddressViewSet, basename="shippingaddress")
router.register("orders", OrderViewSet, basename="orders")
router.register("margins", MarginViewSet, basename="margins")
router.register("products", ProductViewSet, basename="products")
router.register("newproducts", NewProductViewSet, basename="newproducts")
router.register("pingo_orders", PingoOrderViewSet, basename="pingo_orders")
router.register("pingo_items", PingoItemViewSet, basename="pingo_items")


urlpatterns = [
    path("api/", include((router.urls, "store"), namespace="nishiei_ship")),
    path('', cache_page(CACHE_TTL)(HomeView.as_view()), name='home'),
    path('product/<int:pk>/', ProductView.as_view(), name='product'),
    path('search-product/', csrf_exempt(SearchProductView.as_view()), name='search-product'),
    path('order-summary/', OrderSummaryView.as_view(),
         name='order-summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('pingo_checkout/<int:pingoitem_id>/', Pingo_Checkout, name='pingo_checkout'),

    path('api/shoppingcart/', csrf_exempt(ShoppingCartOperation.as_view()), name='api-shoppingcart'),
    path('api/product/get/', csrf_exempt(ProductAPIView.as_view()), name='api-get-product'),
    path('api/categories/', csrf_exempt(CategoryAPIView.as_view()), name='api-get-categories'),
    # path('api/category/products/', csrf_exempt(CategoryProductAPIView.as_view()), name='api-get-category_products'),

    # account related
    # path('account/shippingaddress/', ShippingAddressAPIView.as_view(), name="my_shippingaddress"),
    path('account/orders/', OrderListView.as_view(), name="my_orders"),
    path('account/margins/', MarginListView.as_view(), name="my_margins"),
    path('account/dashboard/', show_dashboard, name="my_dashboard"),
    path('account/addressbook/', AddressBookListView.as_view(), name="my_addressbook"),

    path('export_pdf/<uuid:slug>/', export_pdf_order, name="export_order_pdf"),

]
