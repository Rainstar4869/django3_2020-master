from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import (
    remove_from_cart,
    reduce_quantity_item,
    add_to_cart,
    ProductView,
    SearchProductView,
    HomeView,
    OrderSummaryView,
    CheckoutView,
    AddToChartAPIView,
    ProductAPIView,
    OrderListView
)

app_name = 'store'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:pk>/', ProductView.as_view(), name='product'),
    path('search-product/', csrf_exempt(SearchProductView.as_view()), name='search-product'),
    path('add-to-cart/<int:pk>/<str:location>/', add_to_cart, name='add-to-cart'),
    path('api/add-to-cart/', csrf_exempt(AddToChartAPIView.as_view()), name='api-add-to-cart'),
    path('api/product/get/', csrf_exempt(ProductAPIView.as_view()), name='api-get-product'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(),
         name='order-summary'),
    path('reduce-quantity-item/<int:pk>/', reduce_quantity_item,
         name='reduce-quantity-item'),
    path('checkout/', CheckoutView.as_view(),
         name='checkout'),


    # account related
    path('account/orders/', OrderListView.as_view(), name="my_orders"),

]
