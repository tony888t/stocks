import pytest

from django.urls import reverse
from rest_framework import status

from stock.models import Transaction
from stock.tests.factories import PortfolioFactory, StockFactory


####### HAPPY PATH ######


@pytest.mark.django_db
def test_201_buy_stock(client, investor_user, buy_stock_payload):
    url = reverse("transaction-list")

    # Create stocks
    stock_1 = StockFactory()

    resp = client.post(
        url,
        data=buy_stock_payload,
        headers={"Authorization": f"Token {investor_user.auth_token.key}"},
    )

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json()["stock"] == stock_1.id
    assert resp.json()["quantity"] == buy_stock_payload["quantity"]
    assert resp.json()["transaction_type"] == Transaction.BUY


@pytest.mark.django_db
def test_201_sell_stock(client, investor_user, sell_stock_payload):
    url = reverse("transaction-list")

    # Create stocks
    stock_1 = StockFactory()
    # Create portfolio
    PortfolioFactory(user=investor_user, stock=stock_1, quantity=1000)

    resp = client.post(
        url,
        data=sell_stock_payload,
        headers={"Authorization": f"Token {investor_user.auth_token.key}"},
    )

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json()["stock"] == stock_1.id
    assert resp.json()["quantity"] == sell_stock_payload["quantity"]
    assert resp.json()["transaction_type"] == Transaction.SELL


####### UNHAPPY PATH ######


@pytest.mark.django_db
def test_sell_stock_without_enough_quantity(
    client, investor_user, sell_stock_payload
):
    url = reverse("transaction-list")

    # Create stocks
    stock_1 = StockFactory()
    # Create portfolio
    PortfolioFactory(user=investor_user, stock=stock_1, quantity=1)

    resp = client.post(
        url,
        data=sell_stock_payload,
        headers={"Authorization": f"Token {investor_user.auth_token.key}"},
    )
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    resp_data = resp.json()
    assert resp_data[0] == "Not enough stock to sell"


@pytest.mark.django_db
def test_403_buy_stock(client, admin_user, buy_stock_payload):
    url = reverse("transaction-list")

    # Create stocks
    stock_1 = StockFactory()

    resp = client.post(
        url,
        data=buy_stock_payload,
        headers={"Authorization": f"Token {admin_user.auth_token.key}"},
    )

    assert resp.status_code == status.HTTP_403_FORBIDDEN
