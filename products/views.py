from rest_framework import viewsets

from products.models import Restaurant, Product
from products.serializers import RestaurantSerializer, ProductSerializer


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
