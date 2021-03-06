from rest_framework import serializers

from .models import Category, Product, Variation


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = [
            'id',
            'title',
            'price',
            'sale_price',
        ]

class ProductDetailUpdateSerializer(serializers.ModelSerializer):
    variation_set = VariationSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'image',
            'variation_set',
        ]

    def get_image(self, obj):
        try:
            return obj.productimage_set.first().image.url
        except:
            return None

    def create(self, validated_data):
        title = validated_data['title']
        Product.objects.get(title=title)
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.save()
        return instance

class ProductDetailSerializer(serializers.ModelSerializer):
    variation_set = VariationSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'image',
            'variation_set',
        ]

    def get_image(self, obj):
        try:
            return obj.productimage_set.first().image.url
        except:
            return None

class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product_detail')
    variation_set = VariationSerializer(many=True)
    image = serializers.SerializerMethodField() # read-only field. It gets its value by calling a method on the serializer class it is attached to
                                                # default method it uses is get_<field_name>

    class Meta:
        model = Product
        fields = [
            'url',
            'id',
            'title',
            'description',
            'price',
            'image',
            'variation_set',
        ]

    def get_image(self, obj):
        try:
            return obj.productimage_set.first().image.url
        except:
            return None

class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='category_detail')
    product_set = ProductSerializer(many=True)
    
    class Meta:
        model = Category
        fields = [
            'url',
            'id',
            'title',
            'description',
            'product_set',
            # 'default_category',
        ]