import time

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from bellettrie_library_system.cross_login import my_decrypt
from django.conf import settings

from templogin.models import CrossLogin


def temp_login(request):
    token = request.GET.get('token')
    tt = my_decrypt(token)

    request.session['name'] = tt.name
    request.session['my_id'] = tt.id
    print(tt.perm_level)
    print(CrossLogin.objects.filter(perms_level=tt.perm_level))
    for c in CrossLogin.objects.filter(perms_level=tt.perm_level):
        print(c)
        login(request, c.user)
    return redirect('traffic_light.view')