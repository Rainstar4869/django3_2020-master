from decimal import Decimal
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
import logging
from json import JSONEncoder
import uuid

logger = logging.getLogger("error")


# subclass JSONEncoder
class CartEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding="utf-8")
        return JSONEncoder.default(self, obj)


class Cart(object):

    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {
                "qty": 0,
                "total": 0
            }
        self.cart = cart

        logger.error("current cart")
        logger.error(cart)

    def add(self, product, quantity=1, action=None):
        """
        Add a product to the cart or update its quantity.
        """
        id = product.id
        newItem = True
        if product.id not in self.cart.keys():
            logger.error("new item for cart")
            self.cart[product.id] = {
                'userid': self.request.user.id,
                'product_id': id,
                'name': product.name,
                'quantity': 1,
                'price': str(product.price),
                'image': product.image.url
            }
            self.cart["qty"] += 1
            self.cart["total"] += product.price
        else:
            newItem = True

            for key, value in self.cart.items():
                if key == product.id:
                    logger.error("exist item in cart, and update quantity")
                    value['quantity'] = value['quantity'] + 1
                    newItem = False
                    self.cart["qty"] += 1
                    self.cart["total"] += product.price
                    self.save()
                    break
            if newItem == True:
                logger.error("wired logic here, don't know why")
                self.cart[product.id] = {
                    'userid': self.request,
                    'product_id': product.id,
                    'name': product.name,
                    'quantity': 1,
                    'price': str(product.price),
                    'image': product.image.url
                }

                self.cart["qty"] += 1
                self.cart["total"] += product.price

        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart

        logger.error(" save cart {}".format(str(self.cart)))

        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart["qty"] -= self.cart[product_id]["quantity"]
            self.cart["total"] -= self.cart[product_id]["quantity"] * self.cart[product_id]["quantity"]
            del self.cart[product_id]
            self.save()

    def decrement(self, product):
        for key, value in self.cart.items():
            if key == str(product.id):

                value['quantity'] = value['quantity'] - 1

                self.cart["qty"] -= 1
                self.cart["total"] -= product.price

                if (value['quantity'] < 1):
                    return redirect('cart:cart_detail')

                self.save()
                break
            else:
                print("Something Wrong")

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {
                "qty": 0,
                "total": 0
            }
        self.session.modified = True
