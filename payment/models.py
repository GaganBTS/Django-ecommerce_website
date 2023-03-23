from django.contrib.auth.models import User

from store.models import *


# Create your models here.
class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=255)
    mobile = models.IntegerField()
    address1 = models.CharField(max_length=400)
    landmark = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=140)
    zipcode = models.CharField(max_length=35)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'shipping address'

    def __str__(self):
        return f'Shipping Address - {self.id}'


class Order(models.Model):
    full_name = models.CharField(max_length=255)
    mobile = models.IntegerField()
    shipping_address = models.TextField(max_length=800)
    amount = models.DecimalField(max_digits=8, decimal_places=3)
    date_ordered = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'Order - #{self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=3)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order item - #{self.id}'
