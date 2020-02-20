from django.urls import path
from .controllers import painter_controller


urlpatterns = [
    path('paint', painter_controller.paint, name='paint-image'),
    path('submit-request', painter_controller.submit_request, name='submit-request'),
    path('request-paintings', painter_controller.request_paintings, name='request-paintings'),
    path('request-painting', painter_controller.request_painting, name='request-painting')
]
