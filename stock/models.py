from django.db import models
from django.contrib.auth.models import User


class Stock(models.Model):
    name = models.CharField(max_length=100)
    currency_code = models.CharField(max_length=3)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name", "currency_code")

    def __str__(self):
        return self.name


class Transaction(models.Model):
    BUY = "Buy"
    SELL = "Sell"

    TRANSACTION_CHOICES = [
        (BUY, "Buy"),
        (SELL, "Sell"),
    ]

    investor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="buy_transactions"
    )
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE, related_name="stock"
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=4, choices=TRANSACTION_CHOICES
    )
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.investor.username} - {self.stock.name} - {self.quantity}"
        )


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.stock.name} x {self.quantity}"
