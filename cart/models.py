from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f'Cart {self.id} for {self.user.username}'

    def clear(self):
        self.items.all().delete()

    @property
    def total_price(self):
        return sum([item.total_price for item in self.items.all()])

    @property
    def items_count(self):
        return sum([item.quantity for item in self.items.all()])

    @property
    def items_unique_count(self):
        return self.items.count()

    @property
    def is_empty(self):
        return self.items_unique_count == 0


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')
        unique_together = (
            ['cart', 'product']  # TODO: Do check this when want to add the cart
        )

    def __str__(self):
        return f'{self.quantity} x {self.product.title} in cart {self.cart.id}'

    @property
    def total_price(self):
        return self.product.discount_price * self.quantity
