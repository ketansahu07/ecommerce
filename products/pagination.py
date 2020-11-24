from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response


class ProductPagination(LimitOffsetPagination):
    default_limit = 9
    max_limit = 500
    limit_query_param = 'limit'
    offset_query_param = 'offset'

# these pagination classes are imported in settings.py 

class ProductPagination2(PageNumberPagination):
    page_size = 9
    page_query_param = 'page'
    
    def get_paginated_response(self, data):
        response = {
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'results': data
        }
        return Response(response)