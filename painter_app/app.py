import time
import json
import requests

from tensorflow.keras.applications.vgg19 import VGG19
from google.cloud import pubsub_v1, storage
from .library import painter_engine as engine
from .library import image_helper
from flask import Flask

app = Flask(__name__)

STATUS_CODE_PROCESSING = 2
STATUS_CODE_COMPLETE = 3
STATUS_CODE_FAILED = 4

# TODO: Make these env configs
PUBSUB_PROJECT_ID = 'sylvan-terra-269023'
NEW_PAINTER_REQUEST_TOPIC = 'update-painter-request'

@app.route('/consume-requests')
def consume_requests():
    try:
        pretrained_model = VGG19(include_top=False, weights='imagenet')

        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = 'projects/sylvan-terra-269023/subscriptions/new-painter-request-pull'

        def callback(message):
            try:
                data = message.data.decode('utf-8')
                message.ack()
                json_data = json.loads(data)
                print(json_data)

                # call endpoint on client to update request status to PROCESSING
                update_request_status(json_data['painter_request_id'], STATUS_CODE_PROCESSING)

                # engine.paint(json_data['content_image_path'], pretrained_model)

                update_request_status(json_data['painter_request_id'], STATUS_CODE_COMPLETE)
            except ValueError:
                raise
        future = subscriber.subscribe(subscription_path, callback=callback)

        try:
            future.result()
        except KeyboardInterrupt:
            future.cancel()
    except KeyboardInterrupt:
        raise


def update_request_status(painter_request_id, status_code):
    data = {
        'painter_request_id': painter_request_id,
        'status_code': status_code
    }
    publisher = pubsub_v1.PublisherClient()
    topic_path = 'projects/%s/topics/%s' % (PUBSUB_PROJECT_ID, NEW_PAINTER_REQUEST_TOPIC)
    future = publisher.publish(topic_path, data=json.dumps(data).encode('utf-8'))

    return future.result()


if __name__ == '__main__':
    try:
        consume_requests()
    except Exception:
        exit(1)
