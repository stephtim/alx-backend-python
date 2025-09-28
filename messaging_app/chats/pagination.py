#!/usr/bin/env python3
from rest_framework.pagination import PageNumberPagination


class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'  # optional: clients can request a different page_size
    max_page_size = 100
