from tensorflow.keras.applications import VGG19
from django.http import HttpResponse
from ..painting.painter import Painter
from ..painting.painter_configs import *


def paint(request):
    content_image_path = 'https://i.imgur.com/nwXfz5I.jpg'
    pretrained_model = VGG19(include_top=False, weights='imagenet')
    for i in range(len(PAINTER_CONFIGS)):
        configs = PAINTER_CONFIGS[i]
        painter = Painter(
            pretrained_model,
            configs['CONTENT_LAYERS'],
            configs['STYLE_LAYERS'],
            configs['CONTENT_WEIGHT'],
            configs['STYLE_WEIGHT'])
        painter.paint(content_image_path, configs['STYLE_IMAGE_PATH'])
    return HttpResponse('Finished painting')