from django.http import HttpResponse
from django.core import serializers
from ..models import PainterRequest, RequestPainting


def submit_request(request):
    painter_request = PainterRequest.objects.create(
        content_image_url=request.GET['content_image_url'],
        recipient_email=request.GET['recipient_email'])

    return HttpResponse(painter_request.id)


def get_paintings_for_request(request):
    paintings = RequestPainting.objects.filter(painter_request_id=request.GET['painter_request_id'])
    paintings_serialized = serializers.serialize('json', list(paintings))
    return HttpResponse(paintings_serialized)


def get_painting(request):
    painting = RequestPainting.objects.get(id=request.GET['request_painting_id'])
    painting_serialized = serializers.serialize('json', [painting])
    return HttpResponse(painting_serialized)
