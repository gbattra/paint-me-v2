from django.db import models


class PainterRequest(models.Model):
    is_fulfilled = models.BooleanField(default=False)
    content_image_url = models.CharField(max_length=2048)
    recipient_email = models.CharField(max_length=100)
    date_submitted = models.DateTimeField(auto_now_add=True)
