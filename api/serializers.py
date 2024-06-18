from rest_framework import serializers
from .models import Product, Category, Region, Cart


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'createdAt', 'updatedAt']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'createdAt', 'updatedAt']


class ProductSerializer(serializers.ModelSerializer):
    categoryId = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())
    regionId = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())
    image = serializers.ImageField(
        write_only=True, required=False, allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stockQuantity',
                  'createdAt', 'updatedAt', 'categoryId', 'regionId', 'image']
        
    def create(self, validated_data):
        image_data = validated_data.pop('image', None)
        product = Product.objects.create(**validated_data)
        if image_data:
            product.image = image_data.read()
            product.save()
        return product
        

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'product', 'quantity', 'createdAt', 'updatedAt']
