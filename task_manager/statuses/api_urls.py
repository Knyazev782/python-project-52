from django.urls import path
from .api_views import StatusesAPIDestroy, StatusesAPIUpdate, StatusesAPIList


urlpatterns = [
    path('', StatusesAPIList.as_view()),
    path('<int:pk>/update', StatusesAPIUpdate.as_view()),
    path('<int:pk>/delete', StatusesAPIDestroy.as_view()),
]