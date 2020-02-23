import json
import time


from django.http import HttpResponse
from django.core import serializers
from google.cloud import pubsub_v1
from ..models import PainterRequest, RequestPainting

PUBSUB_PROJECT_ID = 'sylvan-terra-269023'
NEW_PAINTER_REQUEST_TOPIC = 'new-painter-request'


# /submit-request
# - content_image_path (string)
# - recipient_email (string)
def submit_request(request):
    painter_request = PainterRequest.objects.create(
        content_image_path=request.GET['content_image_path'],
        recipient_email=request.GET['recipient_email'])

    data = {
        'painter_request_id': painter_request.id,
        'content_image_path': painter_request.content_image_path
    }
    publisher = pubsub_v1.PublisherClient()
    topic_path = 'projects/%s/topics/%s' % (PUBSUB_PROJECT_ID, NEW_PAINTER_REQUEST_TOPIC)
    future = publisher.publish(topic_path, data=json.dumps(data).encode('utf-8'))

    return HttpResponse(future.result())


# /request-paintings
# - painter_request_id (int)
# - recipient_email (string)
def get_paintings_for_request(request):
    paintings = RequestPainting.objects.filter(painter_request_id=request.GET['painter_request_id'])
    # TODO: check that recipient email matches painting request recipient email
    paintings_serialized = serializers.serialize('json', list(paintings))
    return HttpResponse(paintings_serialized)


# /request-painting
# - request_painting_id (int)
# - recipient_email (string)
def get_painting(request):
    painting = RequestPainting.objects.get(id=request.GET['request_painting_id'])
    # TODO: check that recipient email matches painting request recipient email
    painting_serialized = serializers.serialize('json', [painting])
    return HttpResponse(painting_serialized)


# /update-request-status
# - painter_request_id (int)
# - status_code (int)
def update_requets_status(request):
    status_code = request.GET['status_code']
    painter_request = PainterRequest.objects.get(id=request.GET['painter_request_id'])
    painter_request.status = status_code
    painter_request.save()

    if status_code == PainterRequest.COMPLETED:
        return HttpResponse('Sending email')


# / save-painting
# - painter_request_id (int)
# - generated_image_path (string)
def save_painting(request):
    return RequestPainting.objects.create(
        painter_request_id=request.GET['painter_request_id'],
        generated_image_path=request.GET['generated_image_path']
    )
