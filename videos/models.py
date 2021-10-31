from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.conf import settings
# Create your models here.

# Модель для сохраненеи видеоматериалов
class VideoModel(models.Model):
	tags = TaggableManager()

	author = models.ForeignKey(User, on_delete=models.CASCADE,
							   related_name='video_model')
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, blank=True)
	poster = models.ImageField(upload_to='uploads/%Y/%m/%d')
	upload = models.FileField(upload_to='uploads/%Y/%m/%d')
	body  = models.TextField(blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)

	users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
										related_name='video_like',
										blank=True)
	total_likes = models.PositiveIntegerField(db_index=True,
											  default=0)

	def __str__(self):
		return '{}'.format(self.title)
	
	def get_absolute_url(self):
		return reverse('videos:detail_videos', args=[self.id,
										      self.slug])

class Comment(models.Model):
	video = models.ForeignKey(VideoModel,
							  on_delete=models.CASCADE,
							  related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('created' ,)

	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.video)