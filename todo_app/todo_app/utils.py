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
