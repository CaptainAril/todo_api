from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

# Parameters for task filtering
task_filter_params = [
    OpenApiParameter(
        name="q",
        description="Search query",
        required=False,
        type=OpenApiTypes.STR
    ),
    OpenApiParameter(
        name="status",
        description="Task status",
        required=False,
        type=OpenApiTypes.STR,
    ),
    OpenApiParameter(
        name="priority",
        description="Task priority",
        required=False,
        type=OpenApiTypes.STR,
    ),
]



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


def default_responses(success_schema=None, success_status=200):
    responses = {success_status: success_schema} if success_schema else {}
    responses.update(error_messages)
    return responses