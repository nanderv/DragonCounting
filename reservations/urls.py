from django.urls import path

from . import views

urlpatterns = [
    path('', views.view, name='reserve'),
    path('done', views.view2, name='reserved'),
    path('delete/<slug:id>', views.delete, name='deleted'),
    path('options/<slug:id>/<str:name>', views.options, name='reserve.options'),

]
