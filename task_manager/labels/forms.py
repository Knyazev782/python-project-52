from django import forms
from .models import Labels

class LabelsForm(forms.ModelForm):
    class Meta:
        model = Labels
        fields = ('name',)