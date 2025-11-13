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

    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Introduce tu email'
        })
    )

    city = forms.CharField(
        label='Ciudad de residencia',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Introduce tu ciudad de residencia'
        })
    )

    password = forms.CharField(
        label= 'Password',
        widget= forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Introduce tu contraseña'
        })
    )

    confirm_password = forms.CharField(
        label= 'Confirm Password',
        widget= forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña'
        })
    )

    # Validación para confirmar que las contraseñas coinciden
    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get('password')
        conf = cleaned.get('confirm_password')
        if pwd and conf and pwd != conf:
            self.add_error('confirm_password', 'Las contraseñas no coinciden.')
        return cleaned

    zoo_number = forms.RegexField(
        label='N.º de registro de núcleo zoológico',
        regex=r'^ES\d{2}\d{3}C\d{6}$',
        error_messages={
            'invalid': 'Introduce un número válido, por ejemplo: ES12345C000123.'},
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ejemplo: ES12345C000123'
        })
    )

    class Meta:

        model = User
        fields = ['username', 'email', 'city', 'password', 'zoo_number']