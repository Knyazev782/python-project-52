from django import forms
from .models import Tasks
from task_manager.labels.models import Labels

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name', 'description', 'status', 'assigned_to', 'labels']
        widgets = {
            'labels': forms.SelectMultiple(),
        }
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'assigned_to': 'Исполнитель',
            'labels': 'Метки',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['labels'].queryset = Labels.objects.all()