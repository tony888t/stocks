import pytest
from rest_framework.exceptions import ValidationError

from stock import handler
from stock.tests.factories import PortfolioFactory
from stock.models import Transaction, Portfolio


###### HAPPY PATH ######


@pytest.mark.django_db
def test_handle_portolio_buy_update():
    # Test to see if quantity get updated when stock are bought

    UPDATE_AMOUNT = 5

    portfolio = PortfolioFactory()
    portfolio_id = portfolio.id
    quantity = portfolio.quantity

    handler.handle_portolio_updates(portfolio, Transaction.BUY, UPDATE_AMOUNT)

    portfolio = Portfolio.objects.get(id=portfolio_id)

    # portfolio quantity has been updated by plus UPDATE_AMOUNT
    updated_quantity = quantity + UPDATE_AMOUNT

    assert portfolio.quantity == updated_quantity


@pytest.mark.django_db
def test_handle_portolio_sell_update():
    # Test to see if quantity get updated when stock are sold

    UPDATE_AMOUNT = 5

    portfolio = PortfolioFactory(quantity=65)
    portfolio_id = portfolio.id
    quantity = portfolio.quantity

    handler.handle_portolio_updates(portfolio, Transaction.SELL, UPDATE_AMOUNT)

    portfolio = Portfolio.objects.get(id=portfolio_id)

    # portfolio quantity has been updated by minus UPDATE_AMOUNT
    updated_quantity = quantity - UPDATE_AMOUNT

    assert portfolio.quantity == updated_quantity


###### UNHAPPY PATH ######


@pytest.mark.django_db
def test_handle_portolio_sell_not_enough_quantity():
    # Test handler raises ValidationError if there is not enough stock to sell

    UPDATE_AMOUNT = 5

    portfolio = PortfolioFactory(quantity=2)

    with pytest.raises(ValidationError):
        handler.handle_portolio_updates(
            portfolio, Transaction.SELL, UPDATE_AMOUNT
        )
