from rest_framework.routers import SimpleRouter

from board.views import AdsViewSet
from board.apps import BoardConfig

app_name = BoardConfig.name

router = SimpleRouter()
router.register("", AdsViewSet)

urlpatterns = []

urlpatterns += router.urls