from typing import Any, Dict
from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField( label='Имя пользователя' ,max_length=32)
    password = forms.CharField( label='Пароль' , widget=forms.PasswordInput() )

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        try:
            self.user = User.objects.get(username=username)

        except User.DoesNotExist:
            raise forms.ValidationError(f"Користувача з таким ім'ям {username} не існує!!!")
        
        if not self.user.check_password(password):
            raise forms.ValidationError(f"Невірний пароль!!!")

class RegisterForm(forms.ModelForm):
    age = forms.BooleanField(required=False)
    email = forms.EmailField(max_length=64)
    password = forms.CharField( widget=forms.PasswordInput() )
    class Meta:
        model = User
        fields = ("username", "email", "password")


