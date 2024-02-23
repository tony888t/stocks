from django.contrib import admin
from .models import Stock, Transaction, Portfolio


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    pass
