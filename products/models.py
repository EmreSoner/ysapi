from django.utils.translation import ugettext_lazy as _
from django.db import models

from core.models import StarterModel


class Category(StarterModel):
    name = models.CharField(max_length=64, verbose_name=_('Name'))

    def __str__(self):
        return self.name


class Restaurant(StarterModel):
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return '{} - {}'.format(self.name, self.category.name)


class Product(StarterModel):
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Price'))
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
