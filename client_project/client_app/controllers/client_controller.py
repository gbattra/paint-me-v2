import json
import time


from django.http import HttpResponse
from django.core import serializers
from google.cloud import pubsub_v1
from ..models import PainterRequest, RequestPainting

PUBSUB_PROJECT_ID = 'sylvan-terra-269023'
NEW_PAINTER_REQUEST_TOPIC = 'new-painter-request'


# /submit-request
# - content_image_url (string)
# - recipient_email (string)
def submit_request(request):
    painter_request = PainterRequest.objects.create(
        content_image_url=request.GET['content_image_url'],
        recipient_email=request.GET['recipient_email'])

    data = {
        'painter_request_id': painter_request.id,
        'content_image_url': painter_request.content_image_url
    }
    publisher = pubsub_v1.PublisherClient()
    topic_path = 'projects/%s/topics/%s' % (PUBSUB_PROJECT_ID, NEW_PAINTER_REQUEST_TOPIC)
    future = publisher.publish(topic_path, data=json.dumps(data).encode('utf-8'))

    return HttpResponse(future.result())


# /request-paintings
# - painter_request_id (int)
def get_paintings_for_request(request):
    paintings = RequestPainting.objects.filter(painter_request_id=request.GET['painter_request_id'])
    paintings_serialized = serializers.serialize('json', list(paintings))
    return HttpResponse(paintings_serialized)


# /request-painting
# - request_painting_id (int)
def get_painting(request):
    painting = RequestPainting.objects.get(id=request.GET['request_painting_id'])
    painting_serialized = serializers.serialize('json', [painting])
    return HttpResponse(painting_serialized)
