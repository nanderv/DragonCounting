from django.urls import path

from . import views

urlpatterns = [
    path('status/', views.view, name='traffic_light.view'),
    path('api/', views.crowd_api, name='traffic_light.api'),
    path('diff/<delta>', views.diff, name='traffic_light.diff'),

]
