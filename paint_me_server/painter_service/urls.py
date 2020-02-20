from django.urls import path
from .controllers import painter_controller


urlpatterns = [
    path('', painter_controller.paint, name='paint-image'),
]
