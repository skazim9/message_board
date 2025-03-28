from django.db import models
from users.models import User

class Ads(models.Model):
    title = models.CharField(max_length=255)  # Название товара
    price = models.PositiveIntegerField()  # Цена товара (целое число)
    description = models.TextField()  # Описание товара
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, создавший объявление
    created_at = models.DateTimeField(auto_now_add=True)  # Время и дата создания объявления

    class Meta:
        ordering = ['-created_at']  # Сортировка по дате создания (по убыванию)

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()  # Текст отзыва
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, оставивший отзыв
    ad = models.ForeignKey(Ads, related_name='reviews', on_delete=models.CASCADE)  # Объявление, под которым оставлен отзыв
    created_at = models.DateTimeField(auto_now_add=True)  # Время и дата создания отзыва

    class Meta:
        ordering = ['-created_at']  # Сортировка по дате создания (чем новее, тем выше)

    def __str__(self):
        return f"Review by {self.author.username} on {self.ad.title}"
