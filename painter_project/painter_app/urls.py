from django.urls import path
from .controllers import painter_controller


urlpatterns = [
    path('paint', painter_controller.paint, name='paint')
]
