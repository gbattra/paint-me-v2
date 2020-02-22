import sys
import json

from google.cloud import pubsub_v1
from library import painter_engine as engine


def consume():
    try:
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = 'projects/sylvan-terra-269023/subscriptions/new-painter-request-pull'

        def callback(message):
            try:
                data = message.data.decode('utf-8')
                json_data = json.loads(data)

                # publish / call endpoint on client to update request status to PROCESSING
                engine.paint(json_data['content_image_url'])
                # publish / call endpoint on client to update request status to COMPLETE

                message.ack()
            except ValueError:
                raise

        future = subscriber.subscribe(subscription_path, callback=callback)

        try:
            future.result()
        except KeyboardInterrupt:
            future.cancel()
    except KeyboardInterrupt:
        raise


if __name__ == '__main__':
    try:
        consume()
    except Exception:
        exit(1)
