from django.urls import path
from .controllers import request_controller


urlpatterns = [
    path('', request_controller.submit_request, name='submit-request'),
]
