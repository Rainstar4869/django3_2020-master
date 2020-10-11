from .models import Order, Category
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from .cart import Cart as _Cart
import logging

Logger = logging.getLogger("error-logger")
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def store_categories(request):
    categories = cache.get("nichiei_store_categories")

    if categories is None:
        categories = Category.objects.all()
        cache.set("nichiei_store_categories", categories, CACHE_TTL)

    return {"store_categories": categories}


def session_cart(request):
    return {"session_cart": _Cart(request.session)}
