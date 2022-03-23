from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def main_register(response):
    return render(response, 'registration/register.html')

def register_user(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("/")
    else:
        form = UserCreationForm()
    # POST request: create in users table
    return render(response, 'registration/registeruser.html', {"form": form})

def register_company(response):
    if response.method == "POST":
            form = UserCreationForm(response.POST)
            if form.is_valid():
                form.save()
            return redirect("/")
    else:
        form = UserCreationForm()
    # POST request: create in company table
    return render(response, 'registration/registercompany.html')