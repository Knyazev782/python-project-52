from django.urls import path
from .api_views import TasksAPIList, TasksAPIUpdate, TasksAPIDelete, TasksAPIDetail

urlpatterns = [
    path('', TasksAPIList.as_view(), name='list-task'),
    path('<int:pk>/update', TasksAPIUpdate.as_view(), name='task-update'),
    path('<int:pk>/detail', TasksAPIDetail.as_view(), name='task-detail'),
    path('<int:pk>/delete', TasksAPIDelete.as_view(), name='task-delete'),
]