import pytest

from django.urls import reverse
from rest_framework import status
from stock.tests.factories import PortfolioFactory


@pytest.mark.django_db
def test_200_portfolio(client, investor_user):
    url = reverse("portfolio-list")

    # Create portfolio
    portfolio = PortfolioFactory(user=investor_user)

    resp = client.get(
        url, headers={"Authorization": f"Token {investor_user.auth_token.key}"}
    )

    assert resp.status_code == status.HTTP_200_OK

    resp_data = resp.json()

    assert len(resp_data) == 1  # Only has one portfolio
    assert resp_data[0]["user"] == investor_user.id
    assert resp_data[0]["stock"] == portfolio.stock.id
    assert resp_data[0]["quantity"] == portfolio.quantity


@pytest.mark.django_db
def test_403_portfolio_admin_user(client, admin_user):
    url = reverse("portfolio-list")

    # Create portfolio
    portfolio = PortfolioFactory(user=admin_user)

    resp = client.get(
        url, headers={"Authorization": f"Token {admin_user.auth_token.key}"}
    )

    assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_403_portfolio_generic_user(client, generic_user):
    url = reverse("portfolio-list")

    # Create portfolio
    portfolio = PortfolioFactory(user=generic_user)

    resp = client.get(
        url, headers={"Authorization": f"Token {generic_user.auth_token.key}"}
    )

    assert resp.status_code == status.HTTP_403_FORBIDDEN
