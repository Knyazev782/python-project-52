from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    username = models.CharField(max_length=150, unique=True, verbose_name='Имя пользователя')