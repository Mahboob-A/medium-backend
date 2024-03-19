import pytest

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()

'''
Info On Running Test - Which Field Should Be Tested First 


Running test coverage would give hint which fields should we test / focus on testing more. 
So, before running rest, run a test coverage, check the vurnarable fields, then right test cases. 

After that we can focus on other edge cases to test. 
'''


'''
Run any of the below make command to test with test-coverage result: 


pytest-no-wrn-codecov:
	docker compose -f dev.yml run --rm api pytest -p no:warnigns --cov=. -v  

pytest-no-wrn-codecov-html:
	docker compose -f dev.yml run --rm api pytest -p no:warnigns --cov=. --cov-report html
'''


'''
Test Param: 
Use: normal_user if general user instance is needed. 
Use: super_user if super_user instance is needed. 
User: user_factory is instance is to be created 
'''


@pytest.mark.django_db
def test_create_normal_user(normal_user):
    """
    test function should begin with ' test_ '
    normal_user: the fixer defined in conftest.py

    Test Custom User create is successful
    """
    assert normal_user.first_name is not None
    assert normal_user.last_name is not None
    assert normal_user.email is not None
    assert normal_user.password is not None
    assert normal_user.pkid is not None
    assert normal_user.is_active
    assert not normal_user.is_staff
    assert not normal_user.is_superuser


@pytest.mark.django_db  # use django_db the wrapper for working with database testing
def test_create_super_user(super_user):
    """
    test function should begin with ' test_ '
    super_user: the fixer defined in conftest.py

    Test Custom SuperUser create is successful
    """
    assert super_user.first_name is not None
    assert super_user.last_name is not None
    assert super_user.email is not None
    assert super_user.password is not None
    assert super_user.pkid is not None
    assert super_user.is_active
    assert super_user.is_staff
    assert super_user.is_superuser


@pytest.mark.django_db
def test_get_full_name(normal_user):
    """
    Test Custom User get full name is successfull.
    """
    full_name = normal_user.get_full_name

    expected_full_name = (
        f"{normal_user.first_name.title()} {normal_user.last_name.title()}"
    )

    assert full_name == expected_full_name


@pytest.mark.django_db
def test_get_short_name(normal_user):
    """
    Test Custom User get first name is successfull.
    """
    short_name = normal_user.get_short_name
    assert short_name == normal_user.first_name


@pytest.mark.django_db
def test_update_user(normal_user):
    """
    Test Custom User Update is successfull
    """
    new_first_name = "John"
    new_last_name = "Doe"
    normal_user.first_name = new_first_name
    normal_user.last_name = new_last_name
    normal_user.save()

    updated_user = User.objects.get(pk=normal_user.pk)

    assert updated_user.first_name == new_first_name
    assert updated_user.last_name == new_last_name


@pytest.mark.django_db
def test_delete_user(normal_user):
    """
    Test Custom User deletion is successfull
    """
    user_id = normal_user.id
    normal_user.delete()

    with pytest.raises(User.DoesNotExist):
        User.objects.get(id=user_id)


@pytest.mark.django_db
def test_create_user_without_first_name(user_factory):
    """
    Test Custom User first_name is provided
    """
    with pytest.raises(ValidationError) as err:
        user_factory.create(first_name=None)

    assert "Please provide first name." in str(err.value) 


@pytest.mark.django_db
def test_create_user_without_last_name(user_factory):
    """
    Test Custom User last_name is provided
    """
    with pytest.raises(ValidationError) as err:
        user_factory.create(last_name=None)

    assert "Please provide last name."  in str(err.value)


@pytest.mark.django_db
def test_user_str_repr(normal_user):
    """
    Test Cusom User Model string representation
    """
    assert (
        str(normal_user)
        == f"{normal_user.first_name.title()} {normal_user.last_name.title()}"
    )


@pytest.mark.django_db
def test_normal_user_email_normalized(normal_user):
    """
    Test Custom User email is normalized
    """
    email = normal_user.email
    assert email == email.lower()


@pytest.mark.django_db
def test_user_get_email(normal_user): 
    """
    Test Custom User get_email method is correct
    """
    email = normal_user.email
    assert email == normal_user.get_email 


@pytest.mark.django_db
def test_user_phone_number(normal_user): 
    """
    Test Custom User get_phone_number method is correct
    """
    phone_no = normal_user.phone_number 
    assert phone_no == normal_user.get_phone_number


@pytest.mark.django_db
def test_user_email_incorrect(user_factory):
    """
    Test Custom User email address is correct
    """
    with pytest.raises(ValidationError) as err:
        user_factory.create(email="invalidemail.com")

    #     assert str(err.value) == "Please provide a valid email address." this results the below error 
    # assert "['Please pro...d password.']" == 'Please provi...lid password.' 
    assert "Please provide a valid email address." in str(err.value)


@pytest.mark.django_db
def test_user_with_no_email(user_factory):
    """
    Test Custom User email has not provided
    """
    with pytest.raises(ValidationError) as err:
        user_factory.create(email=None)

    assert "Please provide an email address." in str(err.value) 


@pytest.mark.django_db
def test_user_with_no_password(user_factory):
    """
    Test Custom User password has not provided
    """
    with pytest.raises(ValidationError) as err:
        user_factory.create(password=None)

    assert "Please provide a valid password." in str(err.value) 


# #superuser tests

@pytest.mark.django_db
def test_super_user_email_normalized(super_user):
    """
    Test Custom Super User email is normalized
    """
    email = super_user.email
    assert email == email.lower()


@pytest.mark.django_db
def test_super_user_with_no_email(user_factory):
    """
    Test Custom Super User email has not provided
    """
    with pytest.raises(ValidationError) as err:
        user_factory.create(email=None, is_superuser=True, is_staff=True)

    assert "Please provide an email address." in str(err.value) 


@pytest.mark.django_db
def test_super_user_with_no_password(user_factory):
    """
    Test Custom Super User password has not provided
    """
    with pytest.raises(ValidationError) as err:
        user_factory.create(password=None, is_superuser=True, is_staff=True)

    # to debug set the breakpoint whereever needed.
    # c - until next breakpont
    # q quit
    # n - continue next line
    # type any var to see its value
    # set breakpoint - import pdb; pdb.set_trace()
    
    # #pytest.set_trace()

    assert "Please provide a valid password." in str(err.value) 


@pytest.mark.django_db
def test_super_user_is_not_staff(user_factory):
    """
    Test Custom Super User is not staff
    """
    with pytest.raises(ValidationError) as err:
        user_factory.create(is_superuser=True, is_staff=False)

    assert "Superuser must have is_staff=Ture." in str(err.value) 


@pytest.mark.django_db
def test_super_user_is_not_superuser(user_factory):
    """
    Test Custom Super User is not superuser
    """
    with pytest.raises(ValidationError) as err:
        user_factory.create(is_superuser=False, is_staff=True)
    
    assert "Superuser must have is_superuser=Ture." in  str(err.value)
