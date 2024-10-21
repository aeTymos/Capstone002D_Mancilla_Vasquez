from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as dj_login
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User

@csrf_protect
def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            dj_login(request, user)
            return redirect(to='dashboard')
        else:
            message.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'registration/login.html')