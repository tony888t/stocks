import pytest

from django.urls import reverse
from rest_framework import status
from stock.tests.factories import PortfolioFactory, StockFactory


@pytest.mark.django_db
def test_200_list_all_stocks(client, investor_user):
    url = reverse("stock-list")

    # Create stocks
    stock_1 = StockFactory()
    stock_2 = StockFactory()

    resp = client.get(
        url, headers={"Authorization": f"Token {investor_user.auth_token.key}"}
    )

    assert resp.status_code == status.HTTP_200_OK

    resp_data = resp.json()
    assert len(resp_data) == 2


@pytest.mark.django_db
def test_200_filter_by_name(client, investor_user):
    # Create stocks
    stock_1 = StockFactory(name="test_stock")
    stock_2 = StockFactory()

    url = reverse("stock-list") + f"?search={stock_1.name}"
    resp = client.get(
        url, headers={"Authorization": f"Token {investor_user.auth_token.key}"}
    )

    assert resp.status_code == status.HTTP_200_OK

    resp_data = resp.json()
    assert len(resp_data) == 1

    assert resp_data[0]["name"] == stock_1.name


@pytest.mark.django_db
def test_method_not_allowed(client, investor_user):
    # Create stocks

    payload = {"name": "test", "currency_code": "GBP", "price": 90}

    url = reverse("stock-list")
    resp = client.post(
        url,
        data=payload,
        headers={"Authorization": f"Token {investor_user.auth_token.key}"},
        content_type="application/json",
    )

    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
