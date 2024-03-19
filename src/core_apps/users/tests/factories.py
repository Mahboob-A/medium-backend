import factory
from faker import Factory as FakerFactory

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


faker = FakerFactory().create()

User = get_user_model()


# For testing models that needs to use signals, comment the decorator.
# @factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    email = factory.LazyAttribute(lambda x: faker.email())
    password = factory.LazyAttribute(lambda x: faker.password())
    is_active = True
    is_staff = False

    # def _create_user(self, first_name, last_name, email, password, **extra_fields):
    @classmethod
    def _create(
        cls, model_class, *args, **kwargs
    ):  # Custom User's Manager's create method
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)
