from django.conf import settings
from django.db import models
from django.shortcuts import reverse
import jsonfield
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey
import uuid
import os
import logging

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

    def get_group_count(self):
        cats = self.get_descendants(include_self=False)
        return cats.count()


def image_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("product", filename)


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, upload_to=image_path)
    thumbimage = ImageSpecField(  # 注意：ImageSpecField 不会生成数据库表的字段
        source='image',
        processors=[ResizeToFill(256, 256)],  # 处理成一寸照片的大小
        format='JPEG',  # 处理后的图片格式
        options={'quality': 95}  # 处理后的图片质量
    )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    item_name = models.CharField(max_length=100)
    manufacturer = models.CharField(null=True, blank=True, max_length=50)
    brand = models.CharField(null=True, blank=True, max_length=50)
    series = models.CharField(null=True, blank=True, max_length=50)
    model = models.CharField(null=True, blank=True, max_length=50)

    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    distributor_price = models.IntegerField(blank=True, null=True)
    buy_price = models.IntegerField(blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL, max_length=2)
    description = models.TextField(default="", blank=True, null=True)
    package = models.TextField(default="", blank=True, null=True)
    rate = models.IntegerField(default=5)
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
    order = models.ForeignKey("Order",
                              on_delete=models.CASCADE, related_name="orderitems")
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    final_price = models.IntegerField(null=True, blank=True)
    final_subtotal = models.IntegerField(null=True, blank=True)

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    slug = models.UUIDField(default=uuid.uuid4, unique=True)
    status = models.CharField(choices=ORDER_STATUS, max_length=10, default="NEW")
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    shippingaddress = models.ForeignKey("ShippingAddress", on_delete=models.SET_NULL, blank=True, null=True,
                                        default=None)
    json_orderitems = jsonfield.JSONField(blank=True, null=True, default=None)
    json_shippingaddress = jsonfield.JSONField(blank=True, null=True, default=None)
    Qty = models.IntegerField(blank=True, null=True)
    Total = models.IntegerField(blank=True, null=True)
    message = models.TextField(blank=True, null=True, default="")

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.get_final_price()
        return total

    def get_total_quantity(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.quantity
        return total

    def get_total_distributor_margin(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.get_margin_item_distributor()
        return total

    def get_total_admin_margin(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.get_margin_item_admin()
        return total


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shippingaddress",
                             blank=True, null=True)
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
    is_refound = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "margin to {} from order {}".format(self.user.username, self.order.id)


class PingoItem(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="pingo_items")
    price = models.IntegerField(default=0)
    targetNum = models.IntegerField(default=0)
    currentNum = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    until_at = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, default="description", null=True)

    def __str__(self):
        return "{}, target: {}".format(self.item.item_name, self.targetNum)


class PingoOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pingo_orders")
    product = models.ForeignKey(PingoItem, on_delete=models.CASCADE, related_name="pingo_orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    qty = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    status = models.CharField(default="new", max_length=28)
    paid_at = models.DateTimeField(blank=True, null=True)
    paid_info = models.TextField(blank=True, null=True)
    memo = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{}, product: {}".format(self.user.username, self.product.product.item_name)


@receiver(post_save, sender=Order)
def post_save(sender, instance, created, *args, **kwargs):
    print("post_save Order: ")
    if not created:
        if kwargs is not None and "is_paid" in kwargs['update_fields']:
            margins = Margin.objects.filter(order=instance)
            if margins.exists():
                margins.update(is_valid=instance.is_paid)
