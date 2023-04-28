from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .forms import LoginForm
def register(request):
    return render(request, "auth/register.html")

def login_user(request):
    context = {'login_form': LoginForm()}
    return render(request, "auth/login.html", context)

def logout_user(request):
    logout(request)
    return redirect('index')