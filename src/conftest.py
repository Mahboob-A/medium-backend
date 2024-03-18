import pytest
from pytest_factoryboy import register

from core_apps.users.tests.factories import UserFactory

# by registering the UserFactory, we can use the "user _ factory " fixture in the function.
register(UserFactory)


@pytest.fixture
def normal_user(db, user_factory):
    new_user = user_factory.create()  
    return new_user


@pytest.fixture
def super_user(db, user_factory):
    new_user = user_factory.create(is_superuser=True, is_staff=True)
    return new_user
