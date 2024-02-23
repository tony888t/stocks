from factory import SubFactory
from factory.django import DjangoModelFactory

from django.contrib.auth.models import Group, User


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    name = "Investors"


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = "Test Investor"
    password = "test_Password_123"
    is_superuser = False
