from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Order, OrderItem, Item, Category,ShippingAddress


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        # exclude = ('buy_price','buy_price','buy_price',)
        # fields = "__all__"
        fields = ("id", "item_name", "category", "image", "inventory", "is_valid", "price", "rate",
                  "discount_price", "label", "description")

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result["thumbimage"] = instance.thumbimage.url
        return result


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        exclude = ("user",)


class CategorySerializer(serializers.ModelSerializer):
    full_name = SerializerMethodField("get_full_name")

    class Meta:
        model = Category
        fields = ('id', 'name', 'children', 'full_name')
        # fields = ('id', 'name', 'children', 'full_name')

    def to_representation(self, instance):
        children_nodes = instance.get_descendants(include_self=True)
        product_count = Item.objects.filter(category__in=children_nodes).count()

        result = super().to_representation(instance)
        result["label"] = "{} ({})".format(instance.name, product_count)
        result["show"] = True if product_count else False
        return result

    def get_full_name(self, obj):
        name = obj.name
        if "parent" in self.context:
            parent = self.context["parent"]

            parent_name = self.context["parent_serializer"].get_full_name(parent)

            name = "%s - %s" % (parent_name, name,)
        return name


CategorySerializer._declared_fields['children'] = CategorySerializer(many=True, source='get_children', )
