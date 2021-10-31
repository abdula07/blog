from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.conf import settings 

# Create your models here.

# Менеджер моделя POST
class PublishedManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(status='published')

# Модель для Постов
class Post(models.Model):
	objects = models.Manager()
	published = PublishedManager()
	tags = TaggableManager()
	

	STATUS_CHOICES = (
		('draft', 'Draft'),
		('published', 'Published'),

		)
	


	title = models.CharField(max_length=40)
	slug = models.SlugField(max_length=250, unique_for_date='publish')
	author = models.ForeignKey(User, on_delete=models.CASCADE,
								related_name='blog_posts')
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to="images/%Y/%m/%d", blank=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,
							  choices=STATUS_CHOICES,
							  default='draft')

	users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
										related_name='blog_like',
										blank=True)
	total_likes = models.PositiveIntegerField(db_index=True,
											  default=0)
	
	class Meta:
		ordering = ('-publish' ,)
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post_detail', args=[self.publish.year,
						self.publish.month, self.publish.day, self.slug])

# Модель для комментариев
class Comment(models.Model):
	post = models.ForeignKey(Post, 
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
		return 'Comment by {} on {}'.format(self.name, self.post)

