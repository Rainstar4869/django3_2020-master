import datetime
from django.db.models import Sum
from django.db.models import F
from . import models
import logging
from django.conf import settings

Logger = logging.getLogger("error_logger")
CART_ID = 'CART-ID'


class ItemAlreadyExists(Exception):
    pass


class ItemDoesNotExist(Exception):
    pass


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
            self.session["modified"] = False
        self.cart = cart

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    def add(self, product, quantity=1, action=None):
        id = product.id
        newItem = True
        if product.id not in self.cart.keys():

            self.cart[product.id] = {
                # 'userid': self.request.user.id,
                'product_id': id,
                'name': product.item_name,
                'quantity': quantity,
                'price': product.price,
                'image': product.thumbimage.url
            }
        else:
            newItem = True

            for key, value in self.cart.items():
                if key == product.id:
                    value['quantity'] += quantity
                    newItem = False
                    self.save()
                    break
            if newItem == True:
                self.cart[product.id] = {
                    # 'userid': self.request,
                    'product_id': product.item_name,
                    'name': product.name,
                    'quantity': quantity,
                    'price': product.price,
                    'image': product.thumbimage.url
                }

        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session["modified"] = True

    def remove(self, product):
        if product.id in self.cart:
            del self.cart[product.id]
            self.save()

    def decrement(self, product, quantity=1):
        for key, value in self.cart.items():
            if key == product.id:
                value['quantity'] = value['quantity'] - quantity
                if (value['quantity'] < 1):
                    del self.cart[product.id]
                self.save()
                break
            else:
                print("Something Wrong")

    def clear(self):
        self.cart = self.session[settings.CART_SESSION_ID] = {}
        self.session["modified"] = False

    def update(self, product, quantity, unit_price=None):
        if product.id in self.cart.keys():
            self.cart[product.id] = {
                # 'userid': self.request,
                'product_id': product.id,
                'name': product.name,
                'quantity': quantity,
                'price': product.price,
                'image': product.thumbimage.url
            }

    def count(self):
        quantity = 0
        for key, value in self.cart.items():
            quantity += value["quantity"]

        return quantity

    def summary(self):
        summary = 0
        for key, value in self.cart.items():
            summary += value["quantity"] * value["price"]
        return summary

    def is_empty(self):
        return len(self.cart.items()) == 0

    def cart_serializable(self):
        representation = {}
        for key, value in self.cart.items():
            item_id = key
            item_dict = {
                'sub_total_price': value["quantity"] * value["price"],
                'quantity': value["quantity"],
                "item": value
            }
            representation[item_id] = item_dict
        return representation
