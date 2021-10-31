from django.urls import path
from .import views

app_name = 'videos'

urlpatterns = [
	path('list/', views.list_videos, name='list_videos'),
	path('detail/<int:id_video>/<slug:slug>/',
		 views.detail_videos, name='detail_videos'),
	path('create/', views.create_video,
		 name='create'),
	path('edit/<int:id_video>/', views.edit_video,
		 name='edit'),
	path('videos/', views.my_video,
		 name='my_video'),
	path('video/share/<int:video_id>/', views.video_share,
		 name='video_share'),
	path('like/', views.video_like,
		 name='like')
]