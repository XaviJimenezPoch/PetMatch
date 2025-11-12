from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label= 'Username',
        widget= forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Introduce tu nombre de usuario'
        })
    )

    password = forms.CharField(
        label= 'Password',
        widget= forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Introduce tu contraseña'
        })
    )

    class Meta:

        model = User
        fields = ['username', 'password']