from .serializers import (UserLoginResponseSerializer, UserLoginSerializer,
                          UserLogoutSerializer, UserSerializer,
                          UserSignupSerializer)

error_messages = {
    401: {
        "type": "object",
        "properties": {
            "success": {"type": "boolean", "example": False},
            "message": {"type": "string", "example": "Invalid credentials"},
            }
        },
    400: {
        "type": "object",
        "properties": {
            "success": {"type": "boolean", "example": False},
            "message": {"type": "string", "example": "Bad Request"},
            }
        },
    500: {
        "type": "object",
        "properties": {
            "success": {"type": "boolean", "example": False},
            "message": {"type": "string", "example": "Internal server error"},
            }
        },
    }


UserLoginResponse = {
            200: UserLoginResponseSerializer,
            **error_messages
        }



def default_response(schema):
    return {
        200: schema,
        **error_messages
    }