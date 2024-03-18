from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    def _validate_email(self, email):
        try:
            if not email:
                raise ValidationError(_("Please provide an email address."))
            else:
                email = self.normalize_email(email)
                validate_email(email)
        except ValidationError:
            return ValidationError(_("Please provide a valid email address."))

    def _validate_fields(self, first_name, last_name, email, password):
        if not first_name:
            raise ValidationError(_("Please provide first name."))

        if not last_name:
            raise ValidationError(_("Plese provide last name."))

        if not password:
            raise ValidationError(_("Please provide a valid password."))

        self._validate_email(email=email)

    def _create_user(self, first_name, last_name, email, password, **extra_fields):
        self._validate_fields(
            first_name=first_name, last_name=last_name, email=email, password=password
        )
        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name, last_name=last_name, email=email, **extra_fields
        )

        hashed_password = make_password(password)

        user.password = hashed_password

        user.save(using=self._db)
        return user

    def create_user(self, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is False:
            raise ValidationError(_("Superuser must have is_superuser=Ture."))

        if extra_fields.get("is_staff") is False:
            raise ValidationError(_("Superuser must have is_staff=Ture."))

        return self._create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            **extra_fields,
        )
