from django.db import transaction

from orders.models import Order, OrderItem
from orders.tasks import process_order


class OrderService:
    @staticmethod
    def create_order(user, restaurant, orderitem_set):
        with transaction.atomic():
            amount = sum([order_item['product'].price * order_item['quantity'] for order_item in orderitem_set])
            order = Order.objects.create(user=user, restaurant=restaurant, amount=amount)

            for order_item in orderitem_set:
                for _ in range(0, order_item['quantity']):
                    OrderItem.objects.create(order=order, product=order_item['product'])

        process_order.apply_async((order.id, ))
        return order

    @staticmethod
    def process_order(order, status):
        order.status = status
        order.save()
        return order
