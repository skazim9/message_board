from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apps import BoardConfig
from .views import AdsViewSet, ReviewViewSet

app_name = BoardConfig.name

router = DefaultRouter()
router.register(r"ads", AdsViewSet, basename="ads")
router.register(r"reviews", ReviewViewSet, basename="review")

urlpatterns = [
    path("", include(router.urls)),
]
