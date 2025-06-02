from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Users


class RegistrationUserForm(UserCreationForm):
    class Meta:
        model = Users
        fields = (
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )

class UpdateUserForm(UserChangeForm):
    class Meta:
        model = Users
        fields = (
            'username',
            'first_name',
            'last_name',
        )