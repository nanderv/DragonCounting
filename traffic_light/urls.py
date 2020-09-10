from django.urls import path


from . import views


urlpatterns = [
    path('status/', views.view_light, name='traffic_light.view'),
]
