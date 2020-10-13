from rest_framework import serializers
from .models import Order, OrderItem, Item


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        # exclude = ('buy_price','buy_price','buy_price',)
        # fields = "__all__"
        fields = ("id", "item_name", "category", "image", "inventory", "is_valid", "price",
                  "discount_price", "label", "description")

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result["thumbimage"] = instance.thumbimage.url
        return result
