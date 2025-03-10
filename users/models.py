from django.db import models

from django.contrib.auth.models import AbstractUser
from config.util_models.models import TimeStampModel


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=32, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    def __str__(self):
        return str(self.email)