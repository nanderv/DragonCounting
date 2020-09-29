from django.urls import path

from . import views

urlpatterns = [
    path('', views.view, name='traffic_light.view'),

]
