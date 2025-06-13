from django import forms
from .models import Statuses

class CreateStatusForm(forms.ModelForm):
    class Meta:
        model = Statuses
        fields = ('name',)