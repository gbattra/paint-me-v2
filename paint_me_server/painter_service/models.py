from django.db import models


class PainterRequest(models.Model):
    PENDING = 1
    PROCESSING = 2
    COMPLETED = 3
    FAILED = 4

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed')
    )

    status = models.IntegerField(default=PENDING, choices=STATUS_CHOICES)
    content_image_url = models.CharField(max_length=2048)
    recipient_email = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)


class RequestPainting(models.Model):
    painter_request = models.ForeignKey(PainterRequest, on_delete=models.CASCADE)
    generated_image_url = models.CharField(max_length=2048)
    chosen_by_user = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)