from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def homepage(request):
    return render(request , 'home.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Ensure you have a URL pattern named 'login'
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})  # Corrected template path

def login(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Ensure you have a URL pattern named 'home'
            else:
                form.add_error(None, "Username or password is incorrect")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})  # Corrected template path
