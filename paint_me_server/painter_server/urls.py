from django.urls import path
from . import views


urlpatterns = [
    path('', views.paint, name='paint-image'),
]