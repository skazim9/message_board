from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filters import AdFilter
from .models import Ads, Review
from .paginators import AdsPaginator
from .permissions import IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
from .serializer import AdsSerializer, ReviewSerializer


class AdsViewSet(viewsets.ModelViewSet):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter  # Подключаем фильтры
    pagination_class = AdsPaginator

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_admin:
    #         return Ads.objects.all()
    #     return Ads.objects.filter(author=user)

    def get_permissions(self):
        # Для методов, изменяющих данные
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            if self.request.user and self.request.user.is_staff:  # Проверяем, является ли пользователь администратором
                self.permission_classes = [permissions.IsAuthenticated]  # Администраторы могут всё
            else:
                self.permission_classes = [IsOwnerOrReadOnly]  # Для обычных пользователей
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]  # Анонимные пользователи могут только читать

        return super(AdsViewSet, self).get_permissions()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        # Для методов, изменяющих данные
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            if self.request.user and self.request.user.is_staff:  # Проверяем, является ли пользователь администратором
                self.permission_classes = [permissions.IsAuthenticated]  # Администраторы могут всё
            else:
                self.permission_classes = [IsOwnerOrReadOnly]  # Для обычных пользователей
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]  # Анонимные пользователи могут только читать

        return super(ReviewViewSet, self).get_permissions()
