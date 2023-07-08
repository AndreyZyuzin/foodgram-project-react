from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    """Модель пользователя."""
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        blank=False,
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

    REQUIRED_FIELDS = ['email', 'last_name', 'first_name']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username



class Subscription(models.Model):
    """Модель подписки."""
    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'following'],
                name='unique_following_author',
            )
        ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Автор',
        help_text='Автор',
    )

    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписчики',
        help_text='Подписчики',
    )

    def __str__(self):
        return f'{self.following} подписан на {self.author}'

    def clean(self):
        if self.following.pk == self.author.pk:
            raise ValidationError('Нельза подписаться на себя.')

