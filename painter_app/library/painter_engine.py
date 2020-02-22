from tensorflow.keras.applications.vgg19 import VGG19
from .painter import Painter
from .painter_configs import *


def paint(content_image_url):
    pretrained_model = VGG19(include_top=False, weights='imagenet')
    for i in range(len(PAINTER_CONFIGS)):
        configs = PAINTER_CONFIGS[i]
        painter = Painter(
            pretrained_model,
            configs['CONTENT_LAYERS'],
            configs['STYLE_LAYERS'],
            configs['CONTENT_WEIGHT'],
            configs['STYLE_WEIGHT'])
        image = painter.paint(content_image_url, configs['STYLE_IMAGE_PATH'])

        return image
