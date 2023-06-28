from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Status(models.Choices):
        GUEST = 'guest'
        USER = 'user'
        ADMIN = 'admin'

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        blank=False,
        unique=True,
    )

    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        blank=False,
    )

    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=300,
    )

    role = models.CharField(
        'Роль пользователя',
        max_length=20,
        default=Status.USER,
        choices=Status.choices
    )

    first_name = models.CharField(
        'Имя пользователя',
        blank=True,
        max_length=150,
    )

    last_name = models.CharField(
        'Фамилия пользователя',
        blank=True,
        max_length=150,
    )

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_guest(self):
        return self.role == 'guest'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
