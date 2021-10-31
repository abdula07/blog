from django.shortcuts import render
from blog.models import Post
from videos.models import VideoModel
from django.contrib.postgres.search import SearchVector, SearchQuery, \
										   SearchRank
from .forms import SearchForm
# Create your views here.

def search(request):
	posts = Post.objects.all()
	videos = VideoModel.objects.all()
	form = SearchForm()
	query = None
	results = []
	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data['query']
			search_vector = \
				SearchVector('title', weight='A')\
					+ SearchVector('body', weight='B')
			search_query = SearchQuery(query)
			results = Post.objects.annotate(
						  rank=SearchRank(search_vector, search_query)
						  ).filter(rank__gte=0.3).order_by('-rank')
			results = VideoModel.objects.annotate(
						  rank=SearchRank(search_vector, search_query)
						  ).filter(rank__gte=0.3).order_by('-rank')

	return render(request, 
				  'search/search.html', 
				  {'form': form,
				   'query': query,
				   'results': results,
				   'posts': posts})