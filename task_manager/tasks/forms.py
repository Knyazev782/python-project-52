from django import forms
from .models import Tasks

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name', 'description', 'status', 'author', 'assigned_to', 'labels']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'status': 'Статус',
            'author': 'Автор',
            'assigned_to': 'Исполнитель',
            'labels': 'Метки',
        }