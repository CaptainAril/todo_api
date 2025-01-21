from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None and 'detail' in response.data:
        if response.data.get('code') == 'token_not_valid':
            response.data = {
                "success": False,
                "message": "Token is invalid or expired"
            }
    return response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            **data,
            'meta': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'count': self.page.paginator.count
            }
        })