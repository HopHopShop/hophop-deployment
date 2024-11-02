from django.contrib.auth import get_user_model
from django.db import models

from cart.models import Coupon
from shop.models import Product


class PaymentStatus(models.TextChoices):
    STATUS_PENDING = "Pending"
    STATUS_PAID = "Paid"
    STATUS_CANCELED = "Canceled"
    STATUS_FAILED = "Failed"


class OrderStatus(models.TextChoices):
    STATUS_PENDING = "Pending"
    STATUS_IN_PROGRESS = "In Progress"
    STATUS_IN_TRANSIT = "In Transit"
    STATUS_DELIVERED = "Delivered"
    STATUS_CANCELED = "Canceled"


class Order(models.Model):
    customer = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, null=True, blank=True
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50)
    shipping_address = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=255)
    shipping_postcode = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    payment_type = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(
        max_length=50, choices=PaymentStatus.choices, default=PaymentStatus.STATUS_PENDING
    )
    order_status = models.CharField(
        max_length=50, choices=OrderStatus.choices, default=OrderStatus.STATUS_PENDING
    )
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"

    class Meta:
        ordering = ["-id"]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in order {self.order.id}"