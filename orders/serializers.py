from django.contrib.auth.models import User
from rest_framework import serializers

from orders.models import Order, OrderItem, OrderStatus
from products.models import Product, Restaurant


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    restaurant = RestaurantSerializer()
    orderitem_set = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemCreateSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(required=True, allow_null=False, write_only=True)

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')


class OrderCreateSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemCreateSerializer(
        many=True, required=True, allow_empty=False,
        help_text = """[
            {"product": 5, "quantity": 3},
            {"product": 1, "quantity": 5},
            ...
        """
    )

    class Meta:
        model = Order
        fields = ('user', 'restaurant', 'orderitem_set', )


class OrderProcessSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=[OrderStatus.COMPLETED, OrderStatus.REJECTED],
        required=True,
        help_text="""COMPLETED, REJECTED""")

    class Meta:
        model = Order
        fields = ('status', )
