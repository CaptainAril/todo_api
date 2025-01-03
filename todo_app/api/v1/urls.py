from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import StatusView

router = DefaultRouter()

# router.register('', StatusViewSet, basename='status')

urlpatterns = [
    # path('todo/', TodoViewSet.as_view(), name='todo'),
    path('todo/', include(router.urls)),
    path('status/', StatusView.as_view(), name='status'),
]