# Generated by Django 4.2.3 on 2023-08-30 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commentator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentator_name', models.CharField(max_length=200)),
                ('event_name', models.CharField(max_length=200)),
                ('live_stream_id', models.CharField(blank=True, max_length=200)),
                ('stream_start', models.DateTimeField(blank=True, null=True)),
                ('stream_key', models.CharField(blank=True, max_length=200)),
                ('playback_id', models.CharField(blank=True, max_length=200)),
                ('game_offset', models.IntegerField(blank=True, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
