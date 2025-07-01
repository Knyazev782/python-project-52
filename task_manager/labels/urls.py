from django.urls import path
from . import views

urlpatterns = [
    path('', views.LabelsView.as_view(), name='labels'),
    path('create/', views.CreateLabel.as_view(), name='label_create'),
    path('<int:pk>/update/', views.UpdateLabel.as_view(), name='label_update'),
    path('<int:pk>/delete/', views.DeleteLabel.as_view(), name='label_delete'),
]