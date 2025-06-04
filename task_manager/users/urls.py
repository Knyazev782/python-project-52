from django.urls import path
from task_manager.users import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/create/', views.CreateUserView.as_view(), name='create_users'),
    path('users/<int:pk>/update/', views.UpdateUserView.as_view(), name='update_users'),
    path('users/<int:pk>/delete/', views.DeleteUserView.as_view(), name='delete_users'),
]
