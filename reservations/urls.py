from django.urls import path

from . import views

urlpatterns = [
    path('', views.view, name='reserve'),
    path('register', views.register, name='register'),
]
