from django.db import models


class PainterRequest(models.Model):
    is_fulfilled = models.BooleanField(default=False)
    content_image_url = models.CharField(max_length=2048)
    recipient_email = models.CharField(max_length=100)
    date_submitted = models.DateTimeField(auto_now_add=True)


class RequestPainting(models.Model):
    painter_request = models.ForeignKey(PainterRequest, on_delete=models.CASCADE)
    generated_image = models.ForeignKey('painter_service.GeneratedImage', on_delete=models.CASCADE)
    chosen_by_user = models.BooleanField(default=False)
    date_generated = models.DateTimeField(auto_now_add=True)
