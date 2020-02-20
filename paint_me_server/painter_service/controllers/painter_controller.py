from tensorflow.keras.applications import VGG19
from django.http import HttpResponse
from ..painting.painter import Painter
from ..painting.painter_configs import *
from ..models import PainterRequest


def submit_request(request):
    painter_request = PainterRequest.objects.create(
        content_image_url=request.GET['content_image_url'],
        recipient_email=request.GET['recipient_email'])

    return HttpResponse(painter_request.id)


def paint(request):
    painter_request = PainterRequest.objects.get(id=request.GET['painter_request_id'])
    painter_request.status = PainterRequest.PROCESSING
    painter_request.save()

    pretrained_model = VGG19(include_top=False, weights='imagenet')
    for i in range(len(PAINTER_CONFIGS)):
        configs = PAINTER_CONFIGS[i]
        painter = Painter(
            pretrained_model,
            configs['CONTENT_LAYERS'],
            configs['STYLE_LAYERS'],
            configs['CONTENT_WEIGHT'],
            configs['STYLE_WEIGHT'])
        image = painter.paint('painter_request.content_image_path', configs['STYLE_IMAGE_PATH'])
    return HttpResponse('Finished painting')