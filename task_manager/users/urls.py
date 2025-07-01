from django.urls import path
from . import views

urlpatterns = [
    path('', views.UsersView.as_view(), name='users'),
    path('create/', views.CreateUser.as_view(), name='user_create'),
    path('<int:pk>/update/', views.UpdateUser.as_view(), name='user_update'),
    path('<int:pk>/delete/', views.DeleteUser.as_view(), name='user_delete'),
]