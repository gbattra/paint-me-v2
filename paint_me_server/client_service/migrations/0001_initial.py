# Generated by Django 2.2.5 on 2020-02-20 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PainterRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_fulfilled', models.BooleanField(default=False)),
                ('content_image_url', models.CharField(max_length=2048)),
                ('recipient_email', models.CharField(max_length=100)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
