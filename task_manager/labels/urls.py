from django.urls import path
from . import views

urlpatterns = [
    path('', views.LabelsView.as_view(), name='labels'),
    path('create/', views.CreateLabels.as_view(), name='label_create'),
    path('<int:pk>/update/', views.UpdateLabels.as_view(), name='label_update'),
    path('<int:pk>/delete/', views.DeleteLabels.as_view(), name='label_delete'),
]