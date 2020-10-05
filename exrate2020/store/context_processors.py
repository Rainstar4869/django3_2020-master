from .models import Order, Category


def cart(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, ordered=False)

        if orders.exists():
            order = orders[0]
            return {"cart": order}

    return {"cart": {}}


def store_categories(request):
    categories = Category.objects.all()
    return {"store_categories": categories}
