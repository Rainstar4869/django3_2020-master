from .models import Order


def cart(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, ordered=False)

        if orders.exists():
            order = orders[0]
            return {"cart": order}

    return {"cart": {}}


def cartitem_count(request):
    return {"cartitem_count": 10}
