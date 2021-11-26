from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models

from core.models import StarterModel


class OrderStatus(models.TextChoices):
    WAITING = 'WAITING', _('Waiting')
    COMPLETED = 'COMPLETED', _('Completed')
    REJECTED = 'REJECTED', _('Rejected')


class Order(StarterModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    restaurant = models.ForeignKey('products.Restaurant', on_delete=models.PROTECT)
    amount = models.DecimalField(decimal_places=2, max_digits=12, verbose_name=_('Amount'))
    status = models.CharField(max_length=64, choices=OrderStatus.choices, default=OrderStatus.WAITING)

    def __str__(self):
        return '{}: {}'.format(self.user.get_full_name(), self.amount)


class OrderItem(StarterModel):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT)

    def __str__(self):
        return self.product.name
