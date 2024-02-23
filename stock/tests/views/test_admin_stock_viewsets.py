from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status

from stock.tests.factories import StockFactory
from stock.models import Stock


####### Happy Path #######


@pytest.mark.django_db
def test_admin_get(client, admin_user):
    url = reverse("admin-stock-list")

    # Create stocks
    stock = StockFactory()

    resp = client.get(
        url, headers={"Authorization": f"Token {admin_user.auth_token.key}"}
    )
    assert resp.status_code == status.HTTP_200_OK

    resp_data = resp.json()
    assert len(resp_data) == 1
    assert resp_data[0]["name"] == stock.name
    assert Decimal(resp_data[0]["price"]) == stock.price
    assert resp_data[0]["currency_code"] == stock.currency_code


@pytest.mark.django_db
def test_admin_post(client, admin_user, stock_payload):
    url = reverse("admin-stock-list")

    resp = client.post(
        url,
        data=stock_payload,
        headers={"Authorization": f"Token {admin_user.auth_token.key}"},
        content_type="application/json",
    )
    assert resp.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_admin_patch(client, admin_user):
    url = reverse("admin-stock-list") + "1/"

    # Create stock
    stock = StockFactory()
    patch_payload = {"price": 100}

    resp = client.patch(
        url,
        data=patch_payload,
        headers={"Authorization": f"Token {admin_user.auth_token.key}"},
        content_type="application/json",
    )
    assert resp.status_code == status.HTTP_200_OK

    resp_data = resp.json()

    # Check price has been patched
    assert resp_data["price"] != stock.price
    assert Decimal(resp_data["price"]) == Decimal(patch_payload["price"])


@pytest.mark.django_db
def test_admin_put(client, admin_user, stock_payload):
    url = reverse("admin-stock-list") + "1/"

    # Create stock
    stock = StockFactory(price=50)

    resp = client.put(
        url,
        data=stock_payload,
        headers={"Authorization": f"Token {admin_user.auth_token.key}"},
        content_type="application/json",
    )
    assert resp.status_code == status.HTTP_200_OK

    resp_data = resp.json()

    # Check stock has been patched
    assert resp_data["name"] != stock.name
    assert resp_data["name"] == stock_payload["name"]
    assert resp_data["price"] != stock.price
    assert Decimal(resp_data["price"]) == Decimal(stock_payload["price"])


@pytest.mark.django_db
def test_admin_delete(client, admin_user):
    url = reverse("admin-stock-list") + "1/"

    # Create stock
    stock = StockFactory()

    resp = client.delete(
        url, headers={"Authorization": f"Token {admin_user.auth_token.key}"}
    )
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    # Check stock has been deleted
    stocks = Stock.objects.all()
    assert not stocks
