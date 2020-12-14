from django.urls import path

from . import views

urlpatterns = [
    path('', views.view, name='reserve'),
    path('/options/<slug:id>', views.options, name='reserve.options'),
]
