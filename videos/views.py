from django.shortcuts import render, get_object_or_404
from .models import VideoModel, Comment
from taggit.models import Tag
from django.db.models import Count
from .forms import Videoform, CommentForm, VideoShareForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .tasks import comment_add
from django.core.mail import send_mail
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage,\
								  PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# Create your views here.

# Список видеосов
def list_videos(request):
	videos = VideoModel.objects.all()
	paginator = Paginator(videos, 8)
	page = request.GET.get('page')
	try:
		videos = paginator.page(page)
	except PageNotAnInteger:
		videos = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			return HttpResponse('')
		videos = paginator.page(paginator.num_pages)
	if request.is_ajax():
		return render(request,
					  'videos/videos/list_ajax.html',
					  {'videos': videos})
	return render(request,
				  'videos/videos/list_videos.html',
				  {'videos': videos})

# Детальное преставление видео
def detail_videos(request, id_video, slug, tags_slug=None):
	object_list = VideoModel.objects.all()
	tag = None
	videos = get_object_or_404(VideoModel, 
							   id=id_video,
							   slug=slug)
	if tags_slug:
		tag = get_object_or_404(Tag, slug = tags_slug)
		object_list = object_list.filter(tag__in = [tag])

	# Формирование похожих видеоматеривлов
	videos_tags_ids = videos.tags.values_list('id', flat=True)
	similar_videos = VideoModel.objects.filter(tags__in=videos_tags_ids)\
											   .exclude(id=videos.id)
	similar_videos = similar_videos.annotate(same_tags=Count('tags'))\
											 .order_by('-same_tags')[:4]

	comments = Comment.objects.filter(active=True)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.name = request.user.username
			new_comment.video = videos
			new_comment.save()
			comment_add(new_comment.id)
	else:
		form = CommentForm()

	return render(request,
				  'videos/videos/detail_videos.html',
				  {'videos': videos,
				   'similar_videos': similar_videos,
				   'tag': tag,
				   'form': form,
				   'comments': comments})

	

# Создание видео
@login_required
def create_video(request):
	if request.method == 'POST':
		form = Videoform(data=request.POST,
						 files=request.FILES)
		if form.is_valid():
			new_video = form.save(commit=False)
			new_video.author = request.user
			new_video.save()
			messages.success(request, 'Video added successfully')
		else:
			messages.error(srequest, 'Error adding video')
	else:
		form = Videoform()
	return render(request,
				  'videos/videos/create.html',
				  {'form': form})

# Сортировка видеосов пользователя
@login_required
def my_video(request):
	videos = VideoModel.objects.all()
	my_videos = videos.filter(author=request.user)

	paginator = Paginator(my_videos, 8)
	page = request.GET.get('page')
	try:
		my_videos = paginator.page(page)
	except PageNotAnInteger:
		my_videos = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			return HttpResponse('')
		my_videos = paginator.page(paginator.num_pages)
		
	if request.is_ajax():
		return render(request,
					  'videos/videos/my_videos_ajax.html',
					  {'my_videos': my_videos})

	return render(request,
				  'videos/videos/my_videos.html',
				  {'my_videos': my_videos}) 

# редактирование видеоматериалов
@login_required
def edit_video(request, id_video):
	video = VideoModel.objects.get(id=id_video)
	if request.method == 'POST':
		form = Videoform(instance=video,
						 data=request.POST,
						 files=request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Change saved succesfully')
		else:
			messages.error(request, 'Save Error')
	else:
		form = Videoform(instance=video)
	return render(request,
				  'videos/videos/edit.html',
				  {'form': form})

def video_share(request, video_id):
	video = VideoModel.objects.get(id=video_id)
	sent = False
	if request.method == 'POST':
		form = VideoShareForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			video_url = request.build_absolute_uri(video.get_absolute_url())
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],
															'kajnazarov06@mail.ru',
															video.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(video.title, 
															  video_url,
															  cd['name'],
															  cd['comments'])
			send_mail(subject, message,
					  'kajnazarov06@mail.ru', [cd["to"]])
			sent = True
	else:
		form = VideoShareForm()
	return render(request,
				  'videos/videos/share.html',
				  {'form': form,
				   'video': video,
				   'sent': sent})

@login_required
@require_POST
def video_like(request):
	video_id = request.POST.get('id')
	action = request.POST.get('action')
	try:
		video = VideoModel.objects.get(id=video_id)
		if action == 'like':
			video.users_like.add(request.user)
		else:
			video.users_like.remove(request.user)
		return JsonResponse({'status': 'ok'})
	except:
		pass
	return JsonResponse({'status': 'ok'})