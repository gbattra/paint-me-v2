from django.urls import path
from .controllers import paint_controller


urlpatterns = [
    path('', paint_controller.paint, name='paint-image'),
]
