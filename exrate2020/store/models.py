from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import uuid
import os
from mptt.models import MPTTModel, TreeForeignKey

CATEGORY = (
    ('S', 'Shirt'),
    ('SP', 'Sport Wear'),
    ('OW', 'Out Wear')
)

LABEL = (
    ('N', 'New'),
    ('BS', 'Best Seller')
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
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
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
                             on_delete=models.CASCADE)
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

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    checkout_address = models.ForeignKey("ShippingAddress", on_delete=models.CASCADE, blank=True, null=True)

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
