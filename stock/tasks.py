from random import randrange

from celery import shared_task
from django.db import transaction

# from rest_framework import status

from .models import Stock


def build_randomise_stock_prices() -> dict:
    stocks = Stock.objects.all()
    return {stock: randrange(250) for stock in stocks}


@shared_task
def get_and_update_stock_prices():

    # TODO: add some logic here to fetch stock data via API

    # Assumption: response data and structure
    # {"stock": str, price: num}

    # if response.status_code == status.HTTP_200_OK#

    # TODO: Remove this when adding code to send get request
    resp_data = build_randomise_stock_prices()

    stocks = Stock.objects.all()

    to_update = []

    with transaction.atomic():
        for key, value in resp_data.items():
            Stock.objects.filter(name=key).update(price=value)
