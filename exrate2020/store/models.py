from django.conf import settings
from django.db import models
from django.shortcuts import reverse
import jsonfield
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.db.models.signals import post_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey
import uuid
import os
import logging
import json
from authentication.models import User, Profile
from django.utils.translation import ugettext_lazy as _
from django.core import serializers

logger = logging.getLogger("error")

CATEGORY = (
    ('S', 'Shirt'),
    ('SP', 'Sport Wear'),
    ('OW', 'Out Wear')
)

LABEL = (
    ('N', 'New'),
    ('BS', 'Best Seller')
)

ORDER_STATUS = (
    ("NEW", "NEW"),
    ("FINISHED", "FINISHED"),
)


class Category(MPTTModel):
    name = models.CharField(max_length=64)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return "{}".format(self.name)


def image_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("product", filename)


class Item(models.Model):
    item_name = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    distributor_price = models.IntegerField(blank=True, null=True)
    buy_price = models.IntegerField(blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL, max_length=2)
    description = models.TextField()
    image = models.ImageField(null=True, upload_to=image_path)
    thumbimage = ImageSpecField(  # 注意：ImageSpecField 不会生成数据库表的字段
        source='image',
        processors=[ResizeToFill(256, 256)],  # 处理成一寸照片的大小
        format='JPEG',  # 处理后的图片格式
        options={'quality': 95}  # 处理后的图片质量
    )
    inventory = models.BigIntegerField(default=0, blank=True, null=True)
    is_valid = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse("store:product", kwargs={
            "pk": self.pk
        })

    def get_add_to_cart_url(self):
        return reverse("store:add-to-cart", kwargs={
            "pk": self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("store:remove-from-cart", kwargs={
            "pk": self.pk
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="orderitems")
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_discount_item_price()

    def get_final_item_price(self):
        if self.item.discount_price:
            return self.item.discount_price
        return self.item.price

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()

    def get_total_item_buy_price(self):
        return self.quantity * self.item.buy_price

    def get_total_item_distributor_price(self):
        return self.quantity * self.item.distributor_price

    def get_margin_item_distributor(self):
        if self.item.discount_price:
            return self.get_discount_item_price() - self.get_total_item_distributor_price()
        return self.get_total_item_price() - self.get_total_item_distributor_price()

    def get_margin_item_admin(self):
        return self.get_total_item_distributor_price() - self.get_total_item_buy_price()


class Order(models.Model):
    objects = None
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    uuid = models.UUIDField(default=uuid.uuid4(), editable=False)
    status = models.CharField(choices=ORDER_STATUS, max_length=10, default="NEW")
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    checkout_address = models.ForeignKey("ShippingAddress", on_delete=models.CASCADE, blank=True, null=True)
    json_order = jsonfield.JSONField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_total_quantity(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.quantity
        return total

    def get_total_distributor_margin(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_margin_item_distributor()
        return total

    def get_total_admin_margin(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_margin_item_admin()
        return total


class ShippingAddress(models.Model):
    name = models.CharField(max_length=56)
    email = models.EmailField(max_length=128)
    phone = models.CharField(max_length=56)
    postcode = models.CharField(max_length=20)
    state = models.CharField(max_length=56)
    town = models.CharField(max_length=56)
    street = models.CharField(max_length=128)
    address_1 = models.CharField(max_length=256)
    address_2 = models.CharField(max_length=256)

    def __str__(self):
        return "{}, {}".format(self.name, self.postcode)


class Margin(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="margins")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="margins")
    level = models.IntegerField(default=1)
    amount = models.IntegerField(default=0)
    is_valid = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "margin to {} from order {}".format(self.user.username, self.order.id)


class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name=_('creation date'))
    checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart", default=None)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')
        ordering = ('-creation_date',)

    def __str__(self):
        return str(self.creation_date)


@receiver(post_save, sender=Order)
def post_save(sender, instance, created, update_fields, **kwargs):
    print("print update_fields: ".format(str(update_fields)))
    print("print kwargs: ".format(str(kwargs)))
    print("print created: ".format(str(created)))
    print("print instance: ".format(str(kwargs)))

    if not created:
        if instance.status == "COMPLETED":
            json_order = serializers.serialize('json', Order.objects.filter(pk=instance.id))
            # serializer just one object should add []
            # get model object from json_order as following
            #     orderobj = None
            #     for obj in serializers.deserialize('json', order.json_order):
            #         orderobj = obj.object
            Order.objects.filter(pk=instance.id).update(json_order=json_order)
        else:
            Order.objects.filter(pk=instance.id).update(json_order=None)
