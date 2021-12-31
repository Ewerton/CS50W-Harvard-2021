from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class Base(BaseUserManager):
    use_in_migrations = True

    def __create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('It was not possible to create the account, the email was not informed.'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        return self.__create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Unable to create superuser, is_superuser parameter not set to True.'))

        if extra_fields.get('is_active') is not True:
            raise ValueError(_('Cannot create superuser, parameter is_active has not been set to True.'))

        return self.__create_user(email, password, **extra_fields)
