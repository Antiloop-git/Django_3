from django.db import models
from django.conf import settings
from authapp.models import User

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='basket'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0
    )

    add_datetime = models.DateTimeField(
        verbose_name='время',
        auto_now_add=True
    )

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = Basket.objects.filter(user=self.user)
        _total_quantity = sum([x.quantity for x in _items])
        return _total_quantity

    @property
    def total_cost(self):
        _items = Basket.objects.filter(user=self.user)
        _total_cost = sum([x.product_cost for x in _items])
        return _total_cost