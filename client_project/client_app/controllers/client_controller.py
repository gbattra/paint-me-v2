import json
import time


from django.http import HttpResponse
from django.core import serializers
from google.cloud import pubsub_v1
from ..models import PainterRequest, RequestPainting

PUBSUB_PROJECT_ID = 'sylvan-terra-269023'
NEW_PAINTER_REQUEST_TOPIC = 'new-painter-request'


# WEBAPP ENDPOINT
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


#WEBAPP ENDPOINT
# /request-paintings
# - painter_request_id (int)
# - recipient_email (string)
def get_paintings_for_request(request):
    paintings = RequestPainting.objects.filter(painter_request_id=request.GET['painter_request_id'])
    # TODO: check that recipient email matches painting request recipient email
    paintings_serialized = serializers.serialize('json', list(paintings))
    return HttpResponse(paintings_serialized)


# WEBAPP ENDPOINT
# /request-painting
# - request_painting_id (int)
# - recipient_email (string)
def get_painting(request):
    painting = RequestPainting.objects.get(id=request.GET['request_painting_id'])
    # TODO: check that recipient email matches painting request recipient email
    painting_serialized = serializers.serialize('json', [painting])
    return HttpResponse(painting_serialized)


def update_painter_request_status(request):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = 'projects/sylvan-terra-269023/subscriptions/update-painter-request-status-pull'

    def callback(message):
        try:
            data = message.data.decode('utf-8')
            message.ack()
            json_data = json.loads(data)
            print(json_data)
            status_code = json_data['status_code']
            painter_request = PainterRequest.objects.get(id=json_data['painter_request_id'])
            painter_request.status = status_code
            painter_request.save()

            if status_code == PainterRequest.COMPLETED:
                print("Sending email")
        except ValueError:
            raise
    future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()


def consume_new_paintings(request):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = 'projects/sylvan-terra-269023/subscriptions/save-painting-pull'

    def callback(message):
        try:
            data = message.data.decode('utf-8')
            message.ack()
            json_data = json.loads(data)
            print(json_data)
        except ValueError:
            raise
    future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()
