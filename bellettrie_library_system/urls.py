"""bellettrie_library_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.shortcuts import redirect


def redirect_view(request):
    response = redirect('/crowds/status')
    return response

def robot_view(request):
    return HttpResponse("""User-agent: *
Disallow: /""",content_type='text/plain')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('traffic_light/', include('traffic_light.urls')),
    path('crowds/', include('crowd_counting.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('reserve/', include('reservations.urls')),
    path('', redirect_view, name='homepage.old_link'),
    path('templogin/', include('templogin.urls')),
    path('robots.txt', robot_view, name='robots'),

]
