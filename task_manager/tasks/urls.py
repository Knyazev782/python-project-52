from django.urls import path
from . import views

urlpatterns = [
    path('', views.TasksView.as_view(), name='tasks'),
    path('create/', views.CreateTask.as_view(), name='task_create'),
    path('<int:pk>/update/', views.UpdateTask.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.DeleteTask.as_view(), name='task_delete'),
    path('<int:pk>/', views.DetailTask.as_view(), name='task_detail'),
]