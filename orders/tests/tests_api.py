from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import RequestsClient

from orders.models import Order, OrderStatus
from orders.tests.utils import load_fixture
from products.models import Restaurant


class OrderServiceTestCase(TestCase):
    def setUp(self):
        load_fixture()

    @staticmethod
    def _create_order_api_call():
        user = User.objects.first()
        restaurant = Restaurant.objects.first()
        products = restaurant.product_set.all()

        payload = {
            'user': user.id,
            'restaurant': restaurant.id,
            'orderitem_set': [
                {"product": products[0].id, "quantity": 2},
                {"product": products[1].id, "quantity": 3},
                {"product": products[2].id, "quantity": 5},
            ]
        }

        client = RequestsClient()
        endpoint = 'http://testserver{}'.format(reverse_lazy('order-list'))
        response = client.post(endpoint, json=payload)

        return response

    def test_create_order(self):
        response = self._create_order_api_call()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_process_order(self):
        response = self._create_order_api_call()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        order = Order.objects.first()
        self.assertEqual(order.status, OrderStatus.WAITING)

        endpoint = 'http://testserver{}'.format(reverse_lazy('order-process', kwargs={'pk': order.pk}))
        client = RequestsClient()

        # Invalid Status
        payload = {
            'status': 'Invalid Status'
        }
        response = client.post(endpoint, json=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Valid Status (REJECTED)
        payload = {
            'status': OrderStatus.REJECTED
        }
        response = client.post(endpoint, json=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.first().status, OrderStatus.REJECTED)

        # Valid Status (COMPLETED)
        payload = {
            'status': OrderStatus.COMPLETED
        }
        response = client.post(endpoint, json=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.first().status, OrderStatus.COMPLETED)

