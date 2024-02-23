from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action

from .handler import handle_portolio_updates
from .permissions import IsInvestorOrReadOnly, isAdminOrReadOnly
from .models import Stock, Transaction, Portfolio
from .serializers import (
    StockSerializer,
    TransactionSerializer,
    PortfolioSeriaizer,
)
from django.db import transaction


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

    filterset_fields = ["name"]
    search_fields = ["name"]
    filter_backends = [filters.SearchFilter]
    # ordering_fields = ["name", "price"]
    # ordering = ["name", "-price"]
    permission_classes = [IsInvestorOrReadOnly]


class StockAdminViewSet(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()
    search_fields = ["name", "id"]
    filter_backends = [filters.SearchFilter]

    permission_classes = [isAdminOrReadOnly]


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [IsInvestorOrReadOnly]
    http_method_names = ["post"]

    @transaction.atomic
    def perform_create(self, serializer):
        # TODO: Add logic to work out if investor has enough balance to buy stock
        # TODO: Add logic to update balance if stock is sold

        stock = Stock.objects.get(id=self.request.data["stock"])
        transaction = serializer.save(
            investor=self.request.user, price=stock.price
        )

        investor = transaction.investor
        stock = transaction.stock
        quantity = transaction.quantity
        transaction_type = transaction.transaction_type

        portfolio, created = Portfolio.objects.get_or_create(
            user=investor, stock=stock
        )

        handle_portolio_updates(portfolio, transaction_type, quantity)


class PortfolioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSeriaizer
    permission_classes = [IsInvestorOrReadOnly]

    def get_queryset(self):
        investor = self.request.user

        return Portfolio.objects.filter(user=investor)
