import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.test import APIClient
from django.conf import settings

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123',
        username="test",
        first_name='Test',
        last_name='User'
    )


@pytest.mark.django_db
class TestResetPasswordView:
    def test_reset_password_request_success(self, api_client, user):
        """Успешный запрос на сброс пароля"""
        response = api_client.post('/users/reset_password/', {
            'email': 'test@example.com'
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == "Ссылка для сброса пароля была отправлена на вашу почту."
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == ['test@example.com']
        assert mail.outbox[0].subject == "Сброс пароля"

    def test_reset_password_request_invalid_email(self, api_client):
        """Запрос с несуществующим email"""
        response = api_client.post('/users/reset_password/', {
            'email': 'nonexistent@example.com'
        })
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['error'] == "User not found"
        assert len(mail.outbox) == 0


@pytest.mark.django_db
class TestResetPasswordConfirmView:
    def test_reset_password_confirm_success(self, api_client, user):
        """Успешное подтверждение сброса пароля"""
        # Сначала запрашиваем сброс пароля
        api_client.post('/users/reset_password/', {
            'email': 'test@example.com'
        })

        # Получаем токен и uid из письма
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Подтверждаем сброс пароля
        response = api_client.post('/users/reset_password_confirm/', {
            'uid': uid,
            'token': token,
            'new_password': 'newpass123'
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == "Пароль успешно изменен."

        # Проверяем, что пароль действительно изменился
        user.refresh_from_db()
        assert user.check_password('newpass123')

    def test_reset_password_confirm_invalid_uid(self, api_client):
        """Подтверждение с неверным uid"""
        response = api_client.post('/users/reset_password_confirm/', {
            'uid': 'invalid_uid',
            'token': 'some_token',
            'new_password': 'newpass123'
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == "Ссылка для сброса пароля недействительна."

    def test_reset_password_confirm_invalid_token(self, api_client, user):
        """Подтверждение с неверным токеном"""
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        response = api_client.post('/users/reset_password_confirm/', {
            'uid': uid,
            'token': 'invalid_token',
            'new_password': 'newpass123'
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == "Ссылка для сброса пароля недействительна."

        # Проверяем, что пароль не изменился
        user.refresh_from_db()
        assert user.check_password('testpass123')
