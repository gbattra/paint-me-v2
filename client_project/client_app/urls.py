from django.urls import path
from .controllers import client_controller


urlpatterns = [
    path('submit-request', client_controller.submit_request, name='submit-request'),
    path('request-paintings', client_controller.get_paintings_for_request, name='request-paintings'),
    path('request-painting', client_controller.get_painting, name='request-painting'),
    path('update-request-status', client_controller.update_requets_status, name='update-request-status'),
    path('save-painting', client_controller.save_painting, name='save-painting')
]