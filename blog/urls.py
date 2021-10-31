from django.urls import path
from .import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
	# Обработчики приложения блога.
	path('', views.post_list, name='post_list'),
	# path('', views.PostListView.as_view(), name='post_list'),
	path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

	path('<int:year>/<int:month>/<int:day>/<slug:post>/',
		views.post_detail, name='post_detail'),
	path('<int:post_id>/share/', views.post_share, name='post_share'),
	path('feed/', LatestPostsFeed(), name='post_feed'),

	path('create/', views.create_post, name='create_post'),
	path('my_posts', views.my_posts, name='my_posts'),
	path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),

	path('journal/', views.journal, name='journal'),
	path('like/', views.post_like, name='like')


	
]