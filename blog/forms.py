from django import forms
from .models import Comment, Post

# Форма отправки письмо по email
class EmailPostForm(forms.Form):
	name = forms.CharField(max_length=25)
	#email = forms.EmailField()
	to = forms.EmailField()
	comments = forms.CharField(required=False, widget=forms.Textarea)

# Форма комментирование
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('email', 'body')



# Форма Создание Поста
class CreatePostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('tags', 'title', 'slug',
				  'body', 'publish', 'image',
				  'status')

