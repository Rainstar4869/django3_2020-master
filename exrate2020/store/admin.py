from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Item, OrderItem, Order, ShippingAddress, Category, Margin, PingoItem, PingoOrder

admin.site.register(Item)
admin.site.register(PingoItem)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(PingoOrder)
admin.site.register(ShippingAddress)
admin.site.register(Margin)
admin.site.register(Category, MPTTModelAdmin)
