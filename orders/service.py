from django.db import transaction

from orders.models import Order, OrderItem


class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order(user, restaurant, orderitem_set):
        amount = sum([order_item['product'].price * order_item['quantity'] for order_item in orderitem_set])
        order = Order.objects.create(user=user, restaurant=restaurant, amount=amount)

        for order_item in orderitem_set:
            for _ in range(0, order_item['quantity']):
                OrderItem.objects.create(order=order, product=order_item['product'])

        return order

    @staticmethod
    def process_order(order, status):
        order.status = status
        order.save()
        return order
