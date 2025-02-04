from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from passports.views import *

def authorization(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.success(request, ('Вы ввели неверный логин или пароль!'))
            return redirect('authorization')
    else: 
        return render(request, 'login.html')
    

def exit(request):
    logout(request)
    return redirect('authorization')
