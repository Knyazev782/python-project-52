from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import UsersViewSet, UsersAPIUpdate

router = DefaultRouter()
router.register(r'users', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/users/<int:pk>/', UsersAPIUpdate.as_view()),
]