import tensorflow as tf

from ..lib.painter import Painter
from ..lib.painter_configs import *


def paint(request):
    content_image_path = 'https://i.imgur.com/nwXfz5I.jpg'
    pretrained_model = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
    for i in range(len(PAINTER_CONFIGS)):
        configs = PAINTER_CONFIGS[i]
        painter = Painter(
            pretrained_model,
            configs['CONTENT_LAYERS'],
            configs['STYLE_LAYERS'],
            configs['CONTENT_WEIGHT'],
            configs['STYLE_WEIGHT'])
        painter.paint(content_image_path, configs['STYLE_IMAGE_PATH'])
