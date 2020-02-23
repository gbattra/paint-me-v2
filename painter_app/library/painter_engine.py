import time
import json

from google.cloud import pubsub_v1
from . import image_helper
from .painter import Painter
from .painter_configs import *


PUBSUB_PROJECT_ID = 'sylvan-terra-269023'
SAVE_PAINTING_TOPIC = 'save-painting'


def paint(painter_request_id, content_image_path, pretrained_model):
    for i in range(len(PAINTER_CONFIGS)):
        configs = PAINTER_CONFIGS[i]
        painter = Painter(
            pretrained_model,
            configs['CONTENT_LAYERS'],
            configs['STYLE_LAYERS'],
            configs['CONTENT_WEIGHT'],
            configs['STYLE_WEIGHT'])
        image = painter.paint(content_image_path, configs['STYLE_IMAGE_PATH'])
        filepath = image_helper.save_image(image, 'images/generated')

        publish_painting(painter_request_id, filepath)


def publish_painting(painter_request_id, filepath):
    data = {
        'painter_request_id': painter_request_id,
        'generated_image_path': filepath
    }
    publisher = pubsub_v1.PublisherClient()
    topic_path = 'projects/%s/topics/%s' % (PUBSUB_PROJECT_ID, SAVE_PAINTING_TOPIC)
    future = publisher.publish(topic_path, data=json.dumps(data).encode('utf-8'))

    return future.result()