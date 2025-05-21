from django.db import models
from core.models import TimestampModel


class Order(TimestampModel):
    class PaymentTypeChoices(models.TextChoices):
        IN_PLACE = 'in_place'
        INSTALLMENT = 'installment'
        ONLINE = 'online'

    class StatusChoices(models.TextChoices):
        PENDING = 'pending'
        CANCELLED = 'cancelled'
        COMPLETED = 'completed'

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    address = models.TextField()
    payment_type = models.CharField(max_length=100, choices=PaymentTypeChoices)
    status = models.CharField(max_length=100, choices=StatusChoices, default=StatusChoices.PENDING)

    def __str__(self):
        return f'Order {self.id} user {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField()
