from django.urls import path
from .controllers import client_controller


urlpatterns = [
    path('', client_controller.submit_request, name='submit-request'),
]
