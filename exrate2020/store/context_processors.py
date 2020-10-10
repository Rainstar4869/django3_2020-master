from .models import Order, Category
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def cart(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, ordered=False)

        if orders.exists():
            order = orders[0]
            return {"cart": order}

    return {"cart": {}}


def store_categories(request):
    categories = cache.get("nichiei_store_categories")

    if categories is None:
        categories = Category.objects.all()
        cache.set("nichiei_store_categories", categories, CACHE_TTL)

    return {"store_categories": categories}
