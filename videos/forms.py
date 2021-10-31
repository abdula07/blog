from django import forms
from .models import VideoModel, Comment

# Форма для работы с ВидеоМоделью
class Videoform(forms.ModelForm):
	class Meta:
		model = VideoModel
		fields = (
			'tags', 'title',
			'slug', 'poster',
			'upload', 'body'
			)

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = (
			'email', 'body'
			)

class VideoShareForm(forms.Form):
	name = forms.CharField(max_length=25)
	to = forms.EmailField()
	comments = forms.CharField(required=False, 
							   widget=forms.Textarea)
