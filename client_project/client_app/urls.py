from django.urls import path
from .controllers import client_controller


urlpatterns = [
    path('submit-request', client_controller.submit_request, name='submit-request'),
    path('request-paintings', client_controller.get_paintings_for_request, name='request-paintings'),
    path('request-painting', client_controller.get_painting, name='request-painting'),

    path('consume/painter-request-status-updates',
         client_controller.consume_painter_request_status_update,
         name='consume-painter-request-status-updates'),

    path('consume/new-paintings', client_controller.consume_new_paintings, name='consume-new-paintings')
]