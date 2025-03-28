from rest_framework.serializers import ModelSerializer
from board.models import Ads


class AdsSerializer(ModelSerializer):
    class Meta:
        model = Ads
        fields = "__all__"
