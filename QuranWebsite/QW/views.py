from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def homepage(request):
    return render(request , 'index.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Ensure you have a URL pattern named 'login'
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})  # Corrected template path

from django.contrib.auth import authenticate, login as auth_login

def login_view(request):
    # Initialize an empty message string to capture any specific errors or notifications
    message = ''
    
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Attempt to authenticate the user
            user = authenticate(request, username=username, password=password)
            print('here')
            if user is not None:
                # If authentication was successful, log the user in
                login(request, user)
                # Redirect to the home page or dashboard
                return redirect('home')
            else:
                # If authentication fails, add a non-field error to the form
                form.add_error(None, "Username or password is incorrect")
                message = "Login failed. Please check your username and password."
        else:
            # If the form is invalid, capture the errors as a debug message
            message = "Form validation failed. Please check your input."
            print('here2')
            
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form, "message": message})
