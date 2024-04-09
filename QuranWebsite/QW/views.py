from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm

def homepage(request):
    return HttpResponse('<h1>Welcome to the Quran Website</h1>')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Ensure you have a URL pattern named 'login'
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})  # Corrected template path

def custom_login(request):
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
