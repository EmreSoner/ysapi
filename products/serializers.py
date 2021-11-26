from rest_framework import serializers

from products.models import Category, Restaurant, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Restaurant
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()

    class Meta:
        model = Product
        fields = '__all__'
