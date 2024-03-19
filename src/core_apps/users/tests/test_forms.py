import pytest
from core_apps.users.tests.factories import UserFactory
from core_apps.users.forms import UserCreationForm


@pytest.mark.django_db
def test_user_creation_form_valid_data(): 
    """
    Test UserCreationForm with valid data 
    """
    valid_data = {
        "first_name": "Kemal",
        "last_name": "Soydere",
        "email": "kemal@gmail.com",
        "password1": "testpwd@123",
        "password2": "testpwd@123",
    }
    form = UserCreationForm(valid_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_user_creation_form_invalid_data():
    """
    Test UserCreationForm with invalid data
    """
    user = UserFactory()
    invalid_data = {
        "first_name": "Kemal",
        "last_name": "Soydere",
        "email": user.email,   # email will be already in used. 
        "password1": "testpwd@123",
        "password2": "testpwd@123",
    }

    form = UserCreationForm(invalid_data)
    assert not form.is_valid()
    assert 'email' in form.errors 
