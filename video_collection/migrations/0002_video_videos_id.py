# Generated by Django 4.2.7 on 2023-11-17 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("video_collection", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="video",
            name="videos_id",
            field=models.CharField(default=1, max_length=40, unique=True),
            preserve_default=False,
        ),
    ]
