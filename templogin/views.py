import time

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from bellettrie_library_system.cross_login import my_decrypt
from templogin.models import TempUrl
from django.conf import settings


def temp_login(request):
    token = request.GET.get('token')
    tt = my_decrypt(token).split('|')
    zz = time.time() - float(tt[1])
    if zz < 0 or zz > settings.CROSS_LOGIN_TIMEOUT or tt[2] != settings.CROSS_LOGIN_SECRET:
        return HttpResponse("Token no longer valid")
    request.session['name'] = tt[3];
    return redirect('reserve')