# Generated by Django 3.2.3 on 2021-08-18 08:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos', '0005_rename_video_comment_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='videomodel',
            name='total_likes',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='videomodel',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='video_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
