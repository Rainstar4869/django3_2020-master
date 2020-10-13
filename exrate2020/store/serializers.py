from abc import ABC

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Order, OrderItem, Item, Category


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


class CategorySerializer(serializers.ModelSerializer):
    full_name = SerializerMethodField("get_full_name")

    class Meta:
        model = Category
        fields = ('id', 'name', 'children', 'full_name')

    def get_full_name(self, obj):
        name = obj.name

        if "parent" in self.context:
            parent = self.context["parent"]

            parent_name = self.context["parent_serializer"].get_full_name(parent)

            name = "%s - %s" % (parent_name, name,)

        return name


CategorySerializer._declared_fields['children'] = CategorySerializer(many=True, source='get_children', )
