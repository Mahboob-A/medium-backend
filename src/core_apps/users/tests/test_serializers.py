import pytest


from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from core_apps.users.serializers import UserSerializer, CustomRegisterSerializer


User = get_user_model()


# ## Test Serializer 01: UserSerializer
# comment the mute_signals decorator in the factories.py as failed to do so would yield
# RelatedObjectDoesNotExist (Profile as Profile is being created post_save of CustomUser)  
# does not found error and test will fail.
@pytest.mark.django_db
def test_user_serializer(normal_user):
    """
    Test CusomUser normal user serializer
    """
    serializer = UserSerializer(normal_user)
    assert "id" in serializer.data
    assert "first_name" in serializer.data
    assert "last_name" in serializer.data
    assert "gender" in serializer.data
    assert "profile_id" in serializer.data
    assert "phone_number" in serializer.data
    assert "profile_photo" in serializer.data
    assert "country" in serializer.data
    assert "city" in serializer.data
    assert "twitter_handle" in serializer.data
    assert "total_followers" in serializer.data
    assert "email" in serializer.data


@pytest.mark.django_db
def test_user_to_representation(normal_user):
    """
    Test CusomUser normal user to_representaion
    """
    seiralizer = UserSerializer(normal_user)
    assert "admin" not in seiralizer.data


@pytest.mark.django_db
def test_get_total_followers(normal_user):
    """
    Test CustomUser normal user get_total_followers.
    """
    serializer = UserSerializer(instance=normal_user)
    total_followers = serializer.get_total_followers(normal_user)

    # using the reverse relationship of CustomUser with Profile model.
    #
    assert total_followers == normal_user.profile.followers.count()


@pytest.mark.django_db
def test_super_user_to_representation(super_user):
    """
    Test CusomUser super normal user to_representaion
    """
    seiralizer = UserSerializer(super_user)
    assert "admin" in seiralizer.data
    assert seiralizer.data["admin"] is True


# ## Test Serializer 02: CustomRegisterSerializer


@pytest.mark.django_db
def test_custom_register_seiralizer(mock_request):
    """
    Test CustomRegisterSerializer serializer for Handling HTTP request and user registration
    """

    # Test with valid data
    valid_data = {
        "email": "test@gmail.com",
        "first_name": "Kemal",
        "last_name": "Soydere",
        "password1": "testpwd@123",
        "password2": "testpwd@123",
    }
    serializer = CustomRegisterSerializer(data=valid_data)
    assert serializer.is_valid()

    user = serializer.save(mock_request)
    assert user.email == valid_data.get("email")
    assert user.first_name == valid_data.get("first_name")
    assert user.last_name == valid_data.get("last_name")

    # test with invalid data
    invalid_data = {
        "email": "test@gmail.com",
        "first_name": "Kemal",
        "last_name": "Soydere",
        "password1": "testpwd@123",
        "password2": "wrongpwd@123",
    }
    seiralizer = CustomRegisterSerializer(data=invalid_data)
    with pytest.raises(ValidationError) as err:
        seiralizer.is_valid(raise_exception=True)
