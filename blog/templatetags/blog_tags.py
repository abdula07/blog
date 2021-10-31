from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
register = template.Library()

@register.simple_tag
def total_posts():
	return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
	latest_posts = Post.objects.order_by('-publish')[:count]
	return {'latest_posts': latest_posts}


@register.simple_tag()
def get_most_commented_posts(count=3):
	return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
@register.filter(name='markdown')
def markdown_format(text):
	return mark_safe(markdown.markdown(text))


@register.simple_tag()
def post_title(count=1):
	posts = Post.published.all().order_by('-created')[:count]
	for post in posts:
		post.title
	return post.title

@register.simple_tag()
def post_body(count=1):
	posts = Post.published.annotate().order_by('-created')[:count]

	for post in posts:
		post.body

	return post.body