from rest_framework import serializers
from .models import Stock, Transaction, Portfolio


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("stock", "quantity", "transaction_type")


class PortfolioSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = "__all__"
