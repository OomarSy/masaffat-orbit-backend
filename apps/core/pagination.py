from rest_framework.pagination import PageNumberPagination


class BasePageNumberPagination(PageNumberPagination):
    page_size_query_param = "page_size"


class SmallResultsPagination(BasePageNumberPagination):
    page_size = 10
    max_page_size = 20


class MediumResultsPagination(BasePageNumberPagination):
    page_size = 20
    max_page_size = 50


class LargeResultsPagination(BasePageNumberPagination):
    page_size = 50
    max_page_size = 100
