from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from django.db import models
from .base import Base
# import logging
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from utils.functions import upload_to_path

# logging.basicConfig(**{
#     'handlers': [
#         logging.FileHandler(
#             filename=settings.BASE_DIR / 'logging/user/models/user.log',
#             encoding='utf-8',
#             mode='a+'
#         )
#     ],
#     'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
#     'level': logging.INFO,
#     'datefmt': '%D %T'
# })


class User(AbstractBaseUser, PermissionsMixin):
    objects = Base()
    photo = models.FileField(upload_to=upload_to_path, null=False, blank=False, max_length=1024)
    email = models.EmailField(
        'Email',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name=_('Date joined'), auto_now_add=True, editable=False)
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['id']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def is_admin(self):
        return self.is_superuser

    @property
    def get_email(self):
        return self.email
        
    @property
    def get_photo(self):
        return self.photo
