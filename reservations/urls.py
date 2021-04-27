from django.urls import path

from . import views

urlpatterns = [
    path('', views.view, name='reserve'),
    path('done', views.view2, name='reserved'),
    path('delete/<slug:id>', views.delete, name='deleted'),
    path('logout', views.logout, name='logoutTemp'),

    path('options/<slug:id>/<str:date>', views.options, name='reserve.options'),
    path('force/<slug:id>/<int:d>/<int:to_open>', views.force_timeslot_open, name='reserve.force_timeslot_open'),

]
