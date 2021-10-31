from django.contrib.auth.models import User
from django import forms

# Форма пользователя
class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')

# форма регистрации 
class UserRedistrationForm(forms.ModelForm):
	password = forms.CharField(label='Password',
								 widget=forms.PasswordInput)
	password2 = forms.CharField(label='Repeat password',
								 widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = ('username', 'first_name', 'email')
	# проверка паролей
	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('Password don\'t math')
		return cd['password2']