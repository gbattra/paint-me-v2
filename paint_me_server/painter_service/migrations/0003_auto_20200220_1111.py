# Generated by Django 2.2.5 on 2020-02-20 16:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('painter_service', '0002_styleimage_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PainterRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Processing'), (3, 'Completed'), (4, 'Failed')], default=1)),
                ('content_image_url', models.CharField(max_length=2048)),
                ('recipient_email', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RequestPainting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chosen_by_user', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='generatedimage',
            name='content_image',
        ),
        migrations.RemoveField(
            model_name='generatedimage',
            name='style_image',
        ),
        migrations.AddField(
            model_name='generatedimage',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ContentImage',
        ),
        migrations.DeleteModel(
            name='StyleImage',
        ),
        migrations.AddField(
            model_name='requestpainting',
            name='generated_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='painter_service.GeneratedImage'),
        ),
        migrations.AddField(
            model_name='requestpainting',
            name='painter_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='painter_service.PainterRequest'),
        ),
    ]