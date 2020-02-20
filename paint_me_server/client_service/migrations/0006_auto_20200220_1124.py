# Generated by Django 2.2.5 on 2020-02-20 16:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('client_service', '0005_painterrequest_requestpainting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestpainting',
            name='generated_image',
        ),
        migrations.AddField(
            model_name='requestpainting',
            name='generated_image_url',
            field=models.CharField(default=django.utils.timezone.now, max_length=2048),
            preserve_default=False,
        ),
    ]