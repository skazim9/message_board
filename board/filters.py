import django_filters

from .models import Ads


class AdFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")  # Поиск по названию (буквально)

    class Meta:
        model = Ads
        fields = ["title"]
