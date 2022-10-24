from django.contrib.auth.models import AbstractUser
from django.db import models
from pathlib import Path
from time import time

NULLABLE = {'blank': True, 'null': True}


def users_avatars_path(instanse, filename):
    # file will be uploaded to
    #  MEDIA_ROOT / user_<username> / avatars / <filename>
    num = int(time() * 1000)
    suff = Path(filename).suffix
    return "user_{0}/avatars/{1}".format(instanse.username, f"pic_{num}{suff}")


class User(AbstractUser):
    email = models.EmailField(blank=True, verbose_name="email address", unique=True)
    age = models.PositiveSmallIntegerField(verbose_name="Возраст", **NULLABLE)
    avatar = models.ImageField(upload_to=users_avatars_path, **NULLABLE)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
