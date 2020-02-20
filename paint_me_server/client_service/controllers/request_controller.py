from django.http import HttpResponse


def submit_request(request):
    return HttpResponse('Submitting request')