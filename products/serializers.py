from rest_framework import serializers

from .models import Category, Product

# ProductDetailUpdateSerializer() is to be added

class ProductDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'price',
            'image',
        ]

    def get_image(self, obj):
        return obj.productimage_set.first().image.url

class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-detail')
    image = serializers.SerializerMethodField() # read-only field. It gets its value by calling a method on the serializer class it is attached to
                                                # default method it uses is get_<field_name>

    class Meta:
        model = Product
        fields = [
            'url',
            'id',
            'title',
            'price',
            'image',
        ]

    def get_image(self, obj):
        try:
            return obj.productimage_set.first().image.url
        except:
            return None

class CategorySerializer(serializers.ModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name='category-detail')
    product_set = ProductSerializer(many=True)
    
    class Meta:
        model = Category
        fields = [
            #'url',
            'id',
            'title',
            'description',
            'product_set',
            # 'default_category',
        ]