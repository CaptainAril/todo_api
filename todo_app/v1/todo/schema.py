from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   extend_schema)

from .models import Todo

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
        enum=[status[0] for status in Todo.STATUS_CHOICES],
        required=False,
        type=OpenApiTypes.STR,
    ),
    OpenApiParameter(
        name="priority",
        enum=[priority[0] for priority in Todo.PRIORITY_CHOICES],
        description="Task priority",
        required=False,
        type=OpenApiTypes.STR,
    ),
]

# examples = [
#             OpenApiExample(
#                 "Missing authentication credentials",
#                 summary="Bad Request",
#                 value={"success": False, "message": "Authentication credentials were not provided"},
#             ),
#             OpenApiExample(
#                 "Invalid credentials",
#                 summary="Bad Request",
#                 value={"success": False, "message": "Invalid credentials"}
#             )
#         ]


error_messages = {
    401: {
        "type": "object",
        "properties": {
            "success": {"type": "boolean", "example": False},
            "message": {"type": "string", "example": "Invalid credentials"}, # "Authentication credentials were not provided."
            },
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