from django.contrib.auth.forms import UserCreationForm
from .models import Users

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Users
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )