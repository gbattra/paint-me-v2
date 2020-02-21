from tensorflow.keras.applications import VGG19
from django.http import HttpResponse
from django.core import serializers
from ..painting.painter import Painter
from ..painting.painter_configs import *


def paint(request):
    painter_request_id = request['painter_request_id']

    # publish PROCESSING notificaiton to queue w/ request id

    pretrained_model = VGG19(include_top=False, weights='imagenet')
    for i in range(len(PAINTER_CONFIGS)):
        configs = PAINTER_CONFIGS[i]
        painter = Painter(
            pretrained_model,
            configs['CONTENT_LAYERS'],
            configs['STYLE_LAYERS'],
            configs['CONTENT_WEIGHT'],
            configs['STYLE_WEIGHT'])
        image = painter.paint(request['content_image_url'], configs['STYLE_IMAGE_PATH'])
        # store generated image in cloud storage

        # publish link to image w/ painter request id

    # publish COMPLETED notification to queue w/ request id

    return HttpResponse(True)
