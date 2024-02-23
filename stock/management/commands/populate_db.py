from decimal import Decimal
from rest_framework.authtoken.models import Token

from django.db import transaction
from django.contrib.auth.models import User, Group
from stock.models import Stock

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    @transaction.atomic
    def populate_tables(self):

        admin_group, created = Group.objects.get_or_create(name="Admin")
        investors_group, created = Group.objects.get_or_create(
            name="Investors"
        )

        admin_user = User.objects.create_user(
            username="admin-user", password="adminpassword1122"
        )
        investor_user = User.objects.create_user(
            username="investor-user", password="investorpassword3322"
        )

        # Create Auth Token
        Token.objects.create(user=admin_user)
        Token.objects.create(user=investor_user)

        # Add user to group
        investors_group.user_set.add(investor_user)
        admin_group.user_set.add(admin_user)

        # Create superuser log onto the admin page
        User.objects.create_superuser(
            username="super-user", password="super-secret-password123"
        )

        # Create Stocks
        Stock.objects.get_or_create(
            name="Stock1",
            currency_code="GBP",
            price=Decimal(20),
            description="Stock1 description",
        )
        Stock.objects.get_or_create(
            name="Stock2",
            currency_code="GBP",
            price=Decimal(50),
            description="Stock2 description",
        )

    def handle(self, *args, **options):
        self.populate_tables()
