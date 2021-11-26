import requests
from django.conf import settings
from rest_framework.reverse import reverse_lazy

from orders.models import OrderStatus
from ysapi.celery import app


@app.task
def process_order(order_id):
    endpoint = '{}{}'.format(settings.API_URL, reverse_lazy('order-process', kwargs={'pk': order_id}))
    payload = {
        'status': OrderStatus.COMPLETED
    }

    requests.post(endpoint, payload)
