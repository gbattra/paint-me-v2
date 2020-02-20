from ..lib.painter import Painter
from ..lib.painter_configs import *


def paint(request):
    for i in range(len(PAINTER_CONFIGS)):
        painter = Painter(PAINTER_CONFIGS[i]['CONTENT_LAYERS'], PAINTER_CONFIGS[i]['STYLE_LAYERS'], PAINTER_CONFIGS[i]['CONTENT_WEIGHT'], PAINTER_CONFIGS[i]['STYLE_WEIGHT'])
        content_image_path = 'https://i.imgur.com/nwXfz5I.jpg'
        style_image_path = 'https://i.imgur.com/TltddGV.jpg'
        painter.paint(content_image_path, style_image_path)
