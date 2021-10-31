from django.contrib import admin
from .models import VideoModel
# Register your models here.

# Регистрация ВидеоМодели
@admin.register(VideoModel)
class VideoModelAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug',
					'poster', 'upload',
					'body', 'created']
	