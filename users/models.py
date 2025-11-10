from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Role(models.Model):
    PERMISION_CHOICES = [
        (0, 'Protectora'),
        (1, 'Usuario'),
]