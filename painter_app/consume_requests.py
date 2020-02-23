import time
import json
from tensorflow.keras.applications.vgg19 import VGG19
from google.cloud import pubsub_v1, storage

from library import painter_engine as engine
from library import image_helper

def consume():
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

                img = image_helper.load_img(json_data['content_image_path'])
                image_helper.save_image(image_helper.tensor_to_image(img), 'images/generated')
                # publish / call endpoint on client to update request status to PROCESSING
                # engine.paint(json_data['content_image_path'], pretrained_model)
                # publish / call endpoint on client to update request status to COMPLETE
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
