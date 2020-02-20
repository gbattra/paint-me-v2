from tensorflow.keras.applications import VGG19
from django.http import HttpResponse
from django.core import serializers
from ..painting.painter import Painter
from ..painting.painter_configs import *
from .. import models


def submit_request(request):
    painter_request = models.PainterRequest.objects.create(
        content_image_url=request.GET['content_image_url'],
        recipient_email=request.GET['recipient_email'])

    return HttpResponse(painter_request.id)


def paint(request):
    painter_request = models.PainterRequest.objects.get(id=request.GET['painter_request_id'])
    painter_request.status = models.PainterRequest.PROCESSING
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
        image = painter.paint(painter_request.content_image_url, configs['STYLE_IMAGE_PATH'])
        request_painting = models.RequestPainting.objects.create(
            painter_request=painter_request,
            generated_image_url='generated/image/url')

    painter_request.status = models.PainterRequest.COMPLETED
    painter_request.save()

    return HttpResponse(True)


def request_paintings(request):
    paintings = models.RequestPainting.objects.filter(painter_request_id=request.GET['painter_request_id'])
    paintings_serialized = serializers.serialize('json', list(paintings))
    return HttpResponse(paintings_serialized)


def request_painting(request):
    painting = models.RequestPainting.objects.get(id=request.GET['request_painting_id'])
    painting_serialized = serializers.serialize('json', [painting])
    return HttpResponse(painting_serialized)
