from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Product
from django.contrib.auth.decorators import login_required
from .cart import Cart, CartEncoder
import logging
from django.conf import settings
import json
from django.core import serializers

logger = logging.getLogger("error")


# @api_view(["POST"])
def cart_add(request, id):
    cart = Cart(request)
    logger.error(cart)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    logger.error("print cart of user:")
    logger.error(str(cart))
    return Response({
        "product_id": id,
        "cart2": json.dumps(cart.__dict__)
    })

    logger.error("after add item:")
    logger.error(request.session.get(settings.CART_SESSION_ID))

    return render(request, 'cart/cart_detail.html')


@login_required(login_url="/users/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)

    return redirect("cart_detail")


@login_required(login_url="/users/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/webauth/login")
def cart_detail(request):
    request.session["lionhu"] = "kinghu"
    # request.session[settings.CART_SESSION_ID] = "kinghu"
    # logger.error(request.session[settings.CART_SESSION_ID])
    return render(request, 'cart/cart_detail.html')
