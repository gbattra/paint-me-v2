import time

from . import image_helper
from .painter import Painter
from .painter_configs import *


def paint(content_image_path, pretrained_model):
    for i in range(len(PAINTER_CONFIGS)):
        configs = PAINTER_CONFIGS[i]
        painter = Painter(
            pretrained_model,
            configs['CONTENT_LAYERS'],
            configs['STYLE_LAYERS'],
            configs['CONTENT_WEIGHT'],
            configs['STYLE_WEIGHT'])
        image = painter.paint(content_image_path, configs['STYLE_IMAGE_PATH'])
