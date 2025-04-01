from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Имя пользователя",
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Фамилия пользователя",
    )

    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Укажите почту")

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )

    role = models.CharField(max_length=10, choices=[("user", "User"), ("admin", "Admin")], default="user")

    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
