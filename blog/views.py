from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage,\
								  PageNotAnInteger
from .models import Post, Comment
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, \
								  CreatePostForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .tasks import comment_add
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from videos.models import VideoModel



# Обработчик для отправки письмо по Email
def post_share(request, post_id):
	# Получение статьи по идентификатуру.
	post = get_object_or_404(Post, id=post_id, status='published')
	sent = False
	if request.method == 'POST':
		# Форма была отправлена на сохранение.
		form = EmailPostForm(request.POST)
		if form.is_valid():
			# Все поля формы прошли валидацию
			cd = form.cleaned_data
			# Отправка электронной почты.
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], 
														    'kajnazarov06@mail.ru', 
				                            			    post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, 
															 post_url, 
				               								 cd['name'], 
															 cd['comments'])
			send_mail(subject, message, 
				      'kajnazarov06@mail.ru', [cd['to']])
			sent = True
	else:
		form = EmailPostForm()
	return render(request, 'blog/post/share.html',
				{'post': post, 
				 'form': form, 
				 'sent': sent})

# обработчик для главной страницы
class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'blog/post/list.html'

# обработчик для главной страницы
def post_list(request, tag_slug = None):
	object_list = Post.published.all()
	tag = None

	if tag_slug:
		tag = get_object_or_404(Tag, slug = tag_slug)
		object_list = object_list.filter(tags__in = [tag])		

	paginator = Paginator(object_list, 3) # По 4 статьи на каждой странице.
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# Если страница не является целым числом, возвращаем первую страницу.
		posts = paginator.page(1)
	except EmptyPage:
		# Если намер страницы больше, чем общее количество страниц, возвращаем последнюю.
		posts = paginator.page(paginator.num_pages)
	return render(request, 
				  'blog/post/list.html', 
				  {'page': page, 
				   'posts': posts,
				   'tag': tag})

# обрабочик для детального преставление 
def post_detail(request, year, month, day, post, tag_slug = None):
	object_list = Post.published.all()
	tag = None

	if tag_slug:
		tag = get_object_or_404(Tag, slug = tag_slug)
		object_list = object_list.filter(tags__in = [tag])
	


	post = get_object_or_404(Post, slug=post, 
								   status='published', 
							       publish__year=year,
							       publish__month=month,
							       publish__day=day)
	# Список активных комментариев для этой статьи.
	comments = post.comments.filter(active=True)
	new_comment = None
	if request.method == 'POST':
		# Пользователь отправил комментарий.
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			# Создаем комментарий, но покане сохраняем в базе данных.
			new_comment = comment_form.save(commit=False)
			new_comment.name = request.user.username
			# Привязываем комментарий к текущей статье.
			new_comment.post = post
			# Сохраняем комментарий в базе данных.
			new_comment.save()
			comment_add(new_comment.id)
	else:
		comment_form = CommentForm()

	# Формирование списка похожих статей.
	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Post.published.filter(tags__in = post_tags_ids)\
								  .exclude(id = post.id)
	similar_posts = similar_posts.annotate(same_tags = Count('tags'))\
								  .order_by('-same_tags', '-publish')[:4]

	return render(request, 
		          'blog/post/detail.html', 
		          {'post': post,
				   'comments': comments,
				   'new_comment': new_comment,
				   'comment_form': comment_form,
				   'similar_posts': similar_posts,
				   'tag': tag,})

# обрабочик создание постов
@login_required
def create_post(request):
	if request.method == 'POST':
		create_form = CreatePostForm(data=request.POST,
									 files=request.FILES)
		if create_form.is_valid():
			new_post = create_form.save(commit=False)
			new_post.author = request.user
			new_post.save()
			messages.success(request, 'Post created successfully')
		else:
			messages.error(request, 'Error when creating a post')
	else:
		create_form = CreatePostForm()

	context = {'create_form': create_form}
	return render(request, 
		          'blog/post/create_post.html', 
		         context)

# обрабочик для сортирования личных постов
@login_required
def my_posts(request):
	posts = Post.objects.filter(author=request.user.id)
	paginator = Paginator(posts, 3)
	page = request.GET.get('page')

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			return HttpResponse('')
			posts = paginator.page(paginator.num_pages)

	if request.is_ajax():
		return render(request,
					  'blog/post/my_posts_ajax.html',
					  {'posts': posts})
		
	return render(request, 
		          'blog/post/my_posts.html', 
		          {'posts': posts})

# обрабочик для редактирования постов
@login_required
def edit_post(request, post_id):
	post = Post.objects.get(id=post_id)
	
	if request.method == 'POST':
		post_form = CreatePostForm(instance=post,
								   data=request.POST,
								   files=request.FILES)
		
		if post_form.is_valid():
			post_form.save()
			messages.success(request, 'Post saved successfully')
		else:
			messages.error(request, 'Error while saving post')
	else:
		post_form = CreatePostForm(instance=post)

	return render(request, 
		          'blog/post/edit_post.html', 
		          {'post_form': post_form,
				   'post': post,})

# Обрабочик описание журнала
def journal(request):
	return render(request, 
		          'blog/journal/about_journal.html')

@login_required
@require_POST
def post_like(request):
	post_id = request.POST.get('id')
	action = request.POST.get('action')
	try:
		post = Post.objects.get(id=post_id)
		if action == "like":
			post.users_like.add(request.user)
		else:
			post.users_like.remove(request.user)
		return JsonResponse({'status': 'ok'})
	except:
		pass
	return JsonResponse({'status': 'ok'})


