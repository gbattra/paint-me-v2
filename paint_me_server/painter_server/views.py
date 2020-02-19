from django.shortcuts import render
from django.http import HttpResponse
from .controllers import paint_controller


def paint(request):
    return HttpResponse(paint_controller.paint(request))
