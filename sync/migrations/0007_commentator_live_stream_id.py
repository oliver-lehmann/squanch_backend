# Generated by Django 4.2.3 on 2023-08-25 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sync', '0006_commentator_playback_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentator',
            name='live_stream_id',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
