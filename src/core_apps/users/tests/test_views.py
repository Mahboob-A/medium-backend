import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from core_apps.users.views import CustomUserDetailsView

User = get_user_model()


@pytest.mark.django_db
def test_user_authenticateions(normal_user):
    """'
    Test CustomUser authentication
    """
    # test unauthorized authentication
    client = APIClient()
    url = reverse("user_details")
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # test authorized
    client.force_authenticate(user=normal_user)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_retrive_user_details(normal_user):
    """
    Test CustomUser details with CustomUserDetailsView view
    """
    client = APIClient()
    client.force_authenticate(user=normal_user)
    url = reverse("user_details")
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == normal_user.email
    assert response.data["first_name"] == normal_user.first_name
    assert response.data["last_name"] == normal_user.last_name
    assert response.data["phone_number"] == normal_user.profile.phone_number


@pytest.mark.django_db
def test_user_update_details(normal_user):
    """
    Test CustomUser details update with CustomUserDetailsView view
    """
    client = APIClient()
    client.force_authenticate(user=normal_user)
    url = reverse("user_details")

    updated_first_name = "Updated First Name"
    updated_last_name = "Updated Last Name"
    updated_email_address = "new@gmail.com"
    updated_data = {
        "first_name": updated_first_name,
        "last_name": updated_last_name,
        "email": updated_email_address,
    }
    response = client.patch(url, updated_data)

    # check the response data
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == updated_email_address
    assert response.data["first_name"] == updated_first_name
    assert response.data["last_name"] == updated_last_name

    # check if the user in db has updated
    updated_user = User.objects.get(id=normal_user.id)
    assert updated_user.email == updated_email_address
    assert updated_user.first_name == updated_first_name
    assert updated_user.last_name == updated_last_name


@pytest.mark.django_db
def test_get_queryset_empty(normal_user):
    """
    Test CustomUser CustomUserDetailsView view return empty queryset
    """
    client = APIClient()
    client.force_authenticate(user=normal_user)
    url = reverse("user_details")
    response = client.get(url)

    view = CustomUserDetailsView()
    view.request = response.wsgi_request

    queryset = view.get_queryset()
    expected_queryset_count = 0
    assert queryset.count() == expected_queryset_count
