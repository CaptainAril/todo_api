from django.views import View
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Todo


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