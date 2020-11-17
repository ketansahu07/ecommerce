from rest_framework import serializers

# import orders.models
from product.models import Variation

from .models import CartItem, Cart
# import TokenMixin

class CartVariationSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = Variation
        fields = [
            'id',
            'title',
            'price',
            'product',
        ]

    def get_product(self, obj):
        return obj.product.title

class CartItemSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    item_title = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        field = [
            'item',
            'item_title',
            'price',
            'product',
            'quantity',
            'line_item_total',
        ]

    def get_item(self, obj):
        return obj.item.id
    
    def get_item_title(self, obj):
        return f'{obj.item.product.title} {obj.item.title}'

    def get_product(self, obj):
        return obj.item.product.id
    
    def get_price(self, obj):
        return obj.item.price