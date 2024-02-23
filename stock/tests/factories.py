from random import randrange

from decimal import Decimal
from factory import SubFactory, Faker
from factory.fuzzy import FuzzyChoice
from factory.django import DjangoModelFactory

from stock.models import Stock, Transaction, Portfolio
from users.factories import UserFactory


class StockFactory(DjangoModelFactory):
    class Meta:
        model = Stock

    name = Faker("company")
    currency_code = Faker("currency_code")
    price = Decimal(50)
    description = "Some description"


class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

    investor = SubFactory(UserFactory)
    stock = SubFactory(StockFactory)
    quantity = randrange(100)
    transaction_type = FuzzyChoice(Transaction.TRANSACTION_CHOICES)


class PortfolioFactory(DjangoModelFactory):
    class Meta:
        model = Portfolio

    user = SubFactory(UserFactory)
    stock = SubFactory(StockFactory)
    quantity = randrange(100)
