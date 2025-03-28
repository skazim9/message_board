from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from board.models import Ads
from board.serializer import AdsSerializer


class AdsViewSet(ModelViewSet):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
