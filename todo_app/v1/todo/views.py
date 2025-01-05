from django.db.models import Q
from django.views import View
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from ..users.models import User
from .models import Todo
from .schema import default_responses, error_messages, task_filter_params
from .serializers import TodoCollaboratorSerializer, TodoSerializer


class TodoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class StatusView(APIView):
    def get(self, request):
        todos = Todo.objects.all()
        return Response(
            {
                'status': "OK",
                'code': status.HTTP_200_OK,
                'data': todos.values()
            }
        )
        
@extend_schema(
    responses=default_responses()
)
class TodoViewSet(GenericViewSet):
    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(
            Q(creator=self.request.user) | 
            Q(collaborators=self.request.user)
            ).order_by('-created_at')
    
    permission_classes = [IsAuthenticated]
    pagination_class = TodoPagination

    
    @action(detail=False, methods=['POST'], url_path='create')
    def create_task(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(creator=request.user)
            
            return Response(
                {
                    "success": True,
                    "message": "Todo created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                data={"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
                )
    
    @extend_schema(
        operation_id='get_tasks',
        parameters=task_filter_params,
        responses={
            200: TodoSerializer(many=True),
            400: OpenApiTypes.OBJECT
        },
        
    )
    @action(detail=False, methods=['GET'], url_path='all')
    def get_tasks(self, request):
        # raise NameError('Test error')
        # try:
        todos = self.get_queryset()
        
        q = request.query_params.get('q', None)
        task_status = request.query_params.get('status', None)
        priority = request.query_params.get('priority', None)
        
        if q:
            todos = todos.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)   
            )
            
        if task_status:
            todos = todos.filter(status=task_status)
        if priority:
            todos = todos.filter(priority=priority)
            
        paginator = self.pagination_class()
        paginated_todos = paginator.paginate_queryset(todos, request)
        serializer = self.serializer_class(paginated_todos, many=True)
        
        return paginator.get_paginated_response({
            "success": True,
            "message": "Todos fetched successfully",
            "data": serializer.data
        })
            
        # except Exception as e:
        #     return Response(
        #         data={"success": False, "message": str(e)},
        #         status=status.HTTP_400_BAD_REQUEST
        #         )  
    
    @action(detail=False, methods=['GET'], url_path='(?P<task_id>[0-9]+)')
    def get_task(self, request, **kwargs):
        try:
            pk = kwargs.get('task_id')
            todo = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(todo)
            
            return Response(
                {
                    "success": True,
                    "message": "Todo fetched successfully",
                    "data": serializer.data
                }
            )
        except Exception as e:
            return Response(
                data={"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
                )  
            
    @action(detail=False, methods=['PUT'], url_path='(?P<task_id>[0-9]+)/update')
    def update_task(self, request, **kwargs):
        try:
            pk = kwargs.get('task_id')
            todo = self.get_queryset().get(pk=pk)
            serializer = self.serializer_class(todo, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(
                {
                    "success": True,
                    "message": "Todo updated successfully",
                    "data": serializer.data
                }
            )
        except Exception as e:
            return Response(
                data={"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
                )

    @action(detail=False, methods=['DELETE'], url_path='(?P<task_id>[0-9]+)/delete')
    def delete_task(self, request, **kwargs):
        try:
            pk = kwargs.get('task_id')
            todo = self.get_queryset().get(pk=pk)
            todo.delete()
            
            return Response(
                {
                    "success": True,
                    "message": "Todo deleted successfully",
                }
            )
        except Exception as e:
            return Response(
                data={"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
                )

    @extend_schema(
        request=TodoCollaboratorSerializer,
    )
    @action(detail=False, methods=['POST'], url_path='add-collaborator')
    def add_collaborator(self, request):
        try:
            task_id = request.data.get('task_id')
            # collaborator
            assert task_id, "task_id is required"
            assert request.data.get('collaborator_id'), "collaborator_id is required"
            
            todo = self.get_queryset().get(pk=task_id)
            collaborator = User.objects.get(pk=request.data.get('collaborator_id'))
            
            todo.collaborators.add(collaborator)
            
            return Response(
                data={"success": True, "message": "collaborator added successfully"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                data={"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        request=TodoCollaboratorSerializer,
    )
    @action(detail=False, methods=['POST'], url_path='remove-collaborator')
    def remove_collaborator(self, request):
        try:
            task_id = request.data.get('task_id')
            assert task_id, "task_id is required"
            assert request.data.get('collaborator_id'), "collaborator_id is required"
            
            todo = self.get_queryset().get(pk=task_id)
            collaborator = User.objects.get(pk=request.data.get('collaborator_id'))
            
            todo.collaborators.add(collaborator)
            
            return Response(
                data={"success": True, "message": "collaborator removed successfully"},
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                data={"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
