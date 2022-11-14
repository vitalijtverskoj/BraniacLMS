from pathlib import Path
from time import time

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


def users_avatars_path(instanse, filename):
    # file will be uploaded to
    #  MEDIA_ROOT / user_<username> / avatars / <filename>
    num = int(time() * 1000)
    suff = Path(filename).suffix
    return "user_{0}/avatars/{1}".format(instanse.username, f"pic_{num}{suff}")


class CustomUser(AbstractUser):
    email = models.EmailField(blank=True, verbose_name=_("email address"), unique=True)
    age = models.PositiveSmallIntegerField(verbose_name=_("age"), blank=True, null=True)
    avatar = models.ImageField(upload_to=users_avatars_path, blank=True, null=True, verbose_name=_("avatar"))

    class Meta:
        verbose_name = _('CustomUser')
        verbose_name_plural = _('CustomUsers')
