from rest_framework.exceptions import ValidationError

from .models import Transaction, Portfolio


def handle_portolio_updates(
    portfolio: Portfolio, transaction_type: str, quantity: int
) -> None:
    portfolio_quantity = portfolio.quantity
    if transaction_type == Transaction.SELL:
        if quantity > portfolio_quantity:
            raise ValidationError("Not enough stock to sell")
        else:
            new_quantity = portfolio_quantity - quantity

    else:
        if portfolio_quantity:
            new_quantity = portfolio_quantity + quantity
        else:
            new_quantity = quantity

    portfolio.quantity = new_quantity
    portfolio.save(update_fields=["quantity"])
