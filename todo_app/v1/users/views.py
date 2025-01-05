from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .schema import UserLoginResponse
from .serializers import (UserLoginSerializer, UserLogoutSerializer,
                          UserSerializer, UserSignupSerializer)


class SignUpView(APIView):
    serializer_class = UserSignupSerializer
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(
                data={
                        "success": True,
                        "message": "User created successfully",
                        "data": serializer.data,
                        },
                status=status.HTTP_201_CREATED
                )
            
        except ValidationError as e:
            result = ", \n ".join(f"{key} - {', '.join(value)}" for key, value in e.args[0].items())
            return Response(
                data={"success": False, "message": result},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                data={"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
                )


class LoginView(APIView):
    serializer_class = UserLoginSerializer
    
    @extend_schema(
        request=UserLoginSerializer,
        responses=UserLoginResponse
    )
    def post(self, request):
        try:
            raise NameError('Test error')
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response(
                data={
                    "success": True,
                    "message": "Login successful",
                    "data": serializer.validated_data,
                },
                status=status.HTTP_200_OK)
        
        except AuthenticationFailed as e:
            return Response(
                    data={"success": False, "message": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
                )
        except (ValidationError) as e:
            result = ", \n ".join(f"{key} - {', '.join(value)}" for key, value in e.args[0].items())
            return Response(
                data={"success": False, "message": result},
                status=status.HTTP_400_BAD_REQUEST
            )
        except (Exception) as e:
            return Response(
                data={"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLogoutSerializer
    
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        try:
            serializer = self.serializer_class(data={**request.data, 'refresh': token})
            serializer.is_valid(raise_exception=True)
            
            return Response(
                data={
                    "success": True,
                    "message": serializer.data.get('message'),
                },
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            result = ", \n ".join(f"{key} - {', '.join(value)}" for key, value in e.args[0].items())
            return Response(
                data={"success": False, "message": result},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                data={"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
                )
        
class UserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get(self, request):
        try:
            user = request.user
            serializer = self.serializer_class(user)
            
            return Response(
                data={
                    "success": True,
                    "message": "User retrieved successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                data={"success": False, "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
                )