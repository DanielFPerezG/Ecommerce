from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from base.models import User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'lastName', 'phone', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'lastName', 'phone', 'email']