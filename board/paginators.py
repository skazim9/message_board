from rest_framework.pagination import PageNumberPagination


class AdsPaginator(PageNumberPagination):
    page_size = 4  # пагинация для объявлений
