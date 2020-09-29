from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from templogin.models import TempUrl


def temp_login(request, token):
    code = TempUrl.objects.get(code=token)

    user = User.objects.filter(username='bellettrie').first()
    login(request, user)
    code.delete()
    return redirect('homepage.old_link')