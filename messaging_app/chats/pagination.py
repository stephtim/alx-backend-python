#!/usr/bin/env python3
#!/usr/bin/env python3
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Customize pagination response to explicitly include total count
        via page.paginator.count.
        """
        return Response({
            'count': self.page.paginator.count,   # inserted here
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
