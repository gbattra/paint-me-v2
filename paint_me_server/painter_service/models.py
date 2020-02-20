from django.db import models


class ContentImage(models.Model):
    image_url = models.CharField(max_length=2048)


class StyleImage(models.Model):
    image_url = models.CharField(max_length=2048)


class GeneratedImage(models.Model):
    image_url = models.CharField(max_length=2048)
    content_image = models.ForeignKey(ContentImage, on_delete=models.CASCADE, null=True)
    style_image = models.ForeignKey(StyleImage, on_delete=models.CASCADE)
