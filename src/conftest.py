import pytest
from pytest_factoryboy import register

from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.test import RequestFactory

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


# to user registration serailizer with mock HTTP request object. 
@pytest.fixture
def mock_request(): 
    factory = RequestFactory()
    request = factory.get('/')
    
    ses_middleware = SessionMiddleware(lambda req: None)
    ses_middleware.process_request(request)
    request.session.save()
    
    auth_middleware = AuthenticationMiddleware(lambda req: None)
    auth_middleware.process_request(request)
    
    return request 