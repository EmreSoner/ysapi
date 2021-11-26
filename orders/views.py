from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Order
from orders.serializers import OrderSerializer, OrderCreateSerializer, OrderProcessSerializer
from orders.service import OrderService


class OrderViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):
    queryset = Order.objects.all().select_related('restaurant', 'user').prefetch_related(
        'orderitem_set', 'orderitem_set__product')
    serializer_class = OrderSerializer
    serializer_action_classes = {
        'create': OrderCreateSerializer,
        'process': OrderProcessSerializer,
    }
    service = OrderService()
    filterset_fields = ['status']

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        serializer.instance = self.service.create_order(**validated_data)

    @action(detail=True, methods=['POST'])
    def process(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = self.service.process_order(order, **serializer.validated_data)
        return Response({'status': order.status})


