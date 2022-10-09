import requests
from django.conf import settings
from rest_framework.reverse import reverse_lazy

from orders.models import OrderStatus, Order
from ysapi.celery import app


@app.task
def process_orders_cron():
    orders = Order.objects.filter(status=OrderStatus.WAITING)
    for order in orders:
        process_order.apply_async((order.id, ))


@app.task(
    # RequestException covers ConnectionError, HTTPError, Timeout, TooManyRedirects
    autoretry_for=(requests.exceptions.RequestException,),
    retry_backoff=5,
    max_retries=7,
    retry_jitter=False,
)
def process_order(order_id):
    endpoint = '{}{}'.format(settings.API_URL, reverse_lazy('order-process', kwargs={'pk': order_id}))
    payload = {
        'status': OrderStatus.COMPLETED
    }

    requests.post(endpoint, payload)
