from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LoginView, LogoutView, SignUpView, UserView

router = DefaultRouter()

# router.register('', UserViewSet, basename='user')

urlpatterns = [
    # path('', include(router.urls)),
    
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserView.as_view(), name='user'),
]
