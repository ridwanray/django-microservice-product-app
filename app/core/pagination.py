import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1


import math

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        total_results = self.page.paginator.count
        total_pages = math.ceil(total_results / self.page_size)
        current_page = int(self.request.GET.get('page', DEFAULT_PAGE))
        page_size = int(self.request.GET.get('page_size', self.page_size))

        # Calculate the number of remaining results on the last page
        remaining_results = total_results % page_size

        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': total_results,
            'total_pages': total_pages,
            'current_page': current_page,
            'page_size': page_size if current_page < total_pages else remaining_results,
            'results': data
        })


class StandardResultsPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class StandardResultsPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
