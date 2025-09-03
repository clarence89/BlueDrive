import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        params = self.request.query_params

        page_size = int(params.get('page_size', 10))
        total_count = self.page.paginator.count
        total_pages = math.ceil(total_count/page_size)

        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'next_page': int(params.get('page', 1))+1 if self.page.has_next() else None,
            'previous_page': int(params.get('page', 1))-1 if self.page.has_previous() else None,
            'current_page': int(params.get('page', 1)),
            'total_pages': total_pages,
            'total_count': total_count,
            'current_count': len(data),
            'results': data,
        })