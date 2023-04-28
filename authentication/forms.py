from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField( label='Имя пользователя' ,max_length=32)
    password = forms.CharField(label='Пароль' ,widget=forms.PasswordInput())




