from django import forms
from .models import Tasks

class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = (
            'name',
            'description',
            'assigned_to',
            'status',
        )