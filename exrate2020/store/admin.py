from django.contrib import admin
from .models import Item, OrderItem, Order, ShippingAddress, Category
from mptt.admin import MPTTModelAdmin

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(Category, MPTTModelAdmin)
