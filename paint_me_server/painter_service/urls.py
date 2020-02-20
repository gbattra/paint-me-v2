from django.urls import path
from .controllers import painter_controller


urlpatterns = [
    path('paint/', painter_controller.paint, name='paint-image'),
    path('submit-request/', painter_controller.submit_request, name='submit-request')
]
