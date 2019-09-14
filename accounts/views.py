from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from djongo import models as dmodels
from accounts.models import Account

# Create your views here.

def register(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/register.html', {'error':'Username already exists'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                account = Account()
                account.username = User.objects.get(username=request.POST['username'])
                account.linkset = []
                account.fileset = []
                account.save()
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'accounts/register.html', {'error':'Passwords do not match!'})
    else:
        return render(request, 'accounts/register.html')
    
def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error':'Email or Password is incorrect.'})
    else:
        return render(request, 'accounts/login.html')
    
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')