from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class ProductPagination(LimitOffsetPagination):
    default_limit = 9
    max_limit = 500
    limit_query_param = 'limit'
    offset_query_param = 'offset'