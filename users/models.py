from django.contrib.auth.models import AbstractUser
from django.db import models
from blog.models import NULLABLE
from users.utils import create_token


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)

    code = models.CharField(max_length=50, verbose_name='код', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='Активность')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
