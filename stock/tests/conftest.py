import pytest
from rest_framework.authtoken.models import Token

from stock.models import Transaction
from users.factories import UserFactory, GroupFactory


@pytest.fixture
def investor_user():
    investor_group = GroupFactory()
    user = UserFactory()
    investor_group.user_set.add(user)

    # Create auth token
    token = Token.objects.create(user=user)

    return user


@pytest.fixture
def admin_user():

    admin_group = GroupFactory(name="Admin")
    user = UserFactory()
    admin_group.user_set.add(user)

    # Create auth token
    token = Token.objects.create(user=user)

    return user


@pytest.fixture
def generic_user():
    user = UserFactory()

    # Create auth token
    token = Token.objects.create(user=user)

    return user


@pytest.fixture
def buy_stock_payload():
    return {"stock": 1, "quantity": 10, "transaction_type": Transaction.BUY}


@pytest.fixture
def sell_stock_payload():
    return {"stock": 1, "quantity": 10, "transaction_type": Transaction.SELL}


@pytest.fixture
def stock_payload():
    return {"name": "test_stock", "currency_code": "GBP", "price": 20}
