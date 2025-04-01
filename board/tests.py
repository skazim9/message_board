import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from board.models import Ads, Review
from board.filters import AdFilter

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(
        email='test@example.com',
        username='test',
        password='testpass123'
    )

@pytest.fixture
def ads(user):
    Ads.objects.create(
        title='iPhone 12',
        price=50000,
        description='New iPhone',
        author=user
    )
    Ads.objects.create(
        title='Samsung Galaxy',
        price=30000,
        description='Android phone',
        author=user
    )
    Ads.objects.create(
        title='Xiaomi Phone',
        price=20000,
        description='Chinese phone',
        author=user
    )

@pytest.mark.django_db
class TestAdsFilter:
    def test_filter_by_title(self, ads):
        filter_set = AdFilter({'title': 'iPhone'})
        queryset = filter_set.qs
        assert queryset.count() == 1
        assert queryset.first().title == 'iPhone 12'


    def test_no_filters(self, ads):
        filter_set = AdFilter({})
        queryset = filter_set.qs
        assert queryset.count() == 3

@pytest.fixture
def user():
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123',
        username='test',
        first_name='Test',
        last_name='User'
    )

@pytest.fixture
def ad(user):
    return Ads.objects.create(
        title='Test Ad',
        price=1000,
        description='Test Description',
        author=user
    )

@pytest.mark.django_db
class TestAdsModel:
    def test_create_ad(self, user):
        ad = Ads.objects.create(
            title='Test Ad',
            price=1000,
            description='Test Description',
            author=user
        )
        assert ad.title == 'Test Ad'
        assert ad.price == 1000
        assert ad.description == 'Test Description'
        assert ad.author == user

    def test_ad_str(self, ad):
        assert str(ad) == 'Test Ad'

    def test_ad_ordering(self, user):
        ad1 = Ads.objects.create(
            title='First Ad',
            price=1000,
            description='First Description',
            author=user
        )
        ad2 = Ads.objects.create(
            title='Second Ad',
            price=2000,
            description='Second Description',
            author=user
        )
        ads = Ads.objects.all()
        assert ads[0] == ad2  # Новые объявления должны быть первыми
        assert ads[1] == ad1

@pytest.mark.django_db
class TestReviewModel:
    def test_create_review(self, user, ad):
        review = Review.objects.create(
            text='Test Review',
            author=user,
            ad=ad
        )
        assert review.text == 'Test Review'
        assert review.author == user
        assert review.ad == ad

    def test_review_str(self, user, ad):
        review = Review.objects.create(
            text='Test Review',
            author=user,
            ad=ad
        )
        assert str(review) == f'Review by {user.username} on {ad.title}'

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

@pytest.fixture
def user_token(api_client, user):
    response = api_client.post('/users/login/', {
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    return response.data['access']

@pytest.fixture
def authorized_client(api_client, user_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')
    return api_client

@pytest.fixture
def ad(user):
    return Ads.objects.create(
        title='Test Ad',
        price=1000,
        description='Test Description',
        author=user
    )


@pytest.mark.django_db
class TestAdsViews:
    def test_list_ads_unauthorized(self, api_client):
        response = api_client.get('/board/ads/')
        assert response.status_code == status.HTTP_200_OK


    def test_create_ad_authorized(self, authorized_client):
        response = authorized_client.post('/board/ads/', {
            'title': 'New Ad',
            'price': 2000,
            'description': 'New Description'
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Ad'
        assert response.data['price'] == 2000

    def test_update_ad_author(self, authorized_client, ad):
        response = authorized_client.put(f'/board/ads/{ad.id}/', {
            'title': 'Updated Ad',
            'price': 3000,
            'description': 'Updated Description'
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Ad'
        assert response.data['price'] == 3000

    def test_delete_ad_author(self, authorized_client, ad):
        response = authorized_client.delete(f'/board/ads/{ad.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Ads.objects.filter(id=ad.id).exists()

@pytest.mark.django_db
class TestReviewViews:
    def test_list_reviews_unauthorized(self, api_client, ad):
        response = api_client.get('/board/reviews/')
        assert response.status_code == status.HTTP_200_OK


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


@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        email='admin@example.com',
        password='adminpass123',
        username="admin"
    )


@pytest.fixture
def user_token(api_client, user):
    response = api_client.post('/users/login/', {
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    return response.data['access']


@pytest.fixture
def admin_token(api_client, admin_user):
    response = api_client.post('/users/login/', {
        'email': 'admin@example.com',
        'password': 'adminpass123'
    })
    return response.data['access']


@pytest.fixture
def authorized_client(api_client, user_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')
    return api_client


@pytest.fixture
def admin_client(api_client, admin_token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')
    return api_client


@pytest.fixture
def ad(user):
    return Ads.objects.create(
        title='Test Ad',
        price=1000,
        description='Test Description',
        author=user
    )


@pytest.fixture
def review(user, ad):
    return Review.objects.create(
        text='Test Review',
        author=user,
        ad=ad
    )


@pytest.mark.django_db
class TestReviewPermissions:
    def test_list_reviews_anonymous(self, api_client, review):
        """Анонимные пользователи могут просматривать отзывы"""
        response = api_client.get('/board/reviews/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_update_review_owner(self, authorized_client, review):
        """Владелец может обновлять свой отзыв"""
        response = authorized_client.put(f'/board/reviews/{review.id}/', {
            'text': 'Updated Review',
            'ad': review.ad.id
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] == 'Updated Review'

    def test_update_review_not_owner(self, authorized_client, review):
        """Другой пользователь не может обновлять чужой отзыв"""
        # Создаем другого пользователя
        other_user = User.objects.create_user(
            email='other@example.com',
            username='newuser',
            password='otherpass123'
        )
        other_review = Review.objects.create(
            text='Other Review',
            author=other_user,
            ad=review.ad
        )

        response = authorized_client.put(f'/board/reviews/{other_review.id}/', {
            'text': 'Updated Review',
            'ad': other_review.ad.id
        })
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_review_owner(self, authorized_client, review):
        """Владелец может удалять свой отзыв"""
        response = authorized_client.delete(f'/board/reviews/{review.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Review.objects.filter(id=review.id).exists()

    def test_delete_review_not_owner(self, authorized_client, review):
        """Другой пользователь не может удалять чужой отзыв"""
        # Создаем другого пользователя
        other_user = User.objects.create_user(
            email='other@example.com',
            username='newtestuser',
            password='otherpass123'
        )
        other_review = Review.objects.create(
            text='Other Review',
            author=other_user,
            ad=review.ad
        )

        response = authorized_client.delete(f'/board/reviews/{other_review.id}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Review.objects.filter(id=other_review.id).exists()

    def test_admin_can_update_any_review(self, admin_client, review):
        """Администратор может обновлять любой отзыв"""
        response = admin_client.put(f'/board/reviews/{review.id}/', {
            'text': 'Updated by Admin',
            'ad': review.ad.id
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] == 'Updated by Admin'

    def test_admin_can_delete_any_review(self, admin_client, review):
        """Администратор может удалять любой отзыв"""
        response = admin_client.delete(f'/board/reviews/{review.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Review.objects.filter(id=review.id).exists()
