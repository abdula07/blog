from django.shortcuts import render
from .forms import UserForm, UserRedistrationForm

# Create your views here.

# обработчик профиля пользователя
def my_account(request):
	return render(request, 
				  'profile/my_account.html')

# Обработчик редактирование аккаунта
def edit_account(request):
	if request.method == 'POST':
		user_form = UserForm(instance=request.user, 
						data=request.POST)
		if user_form.is_valid():
			user_form.save()
	else:
		user_form = UserForm(instance=request.user)
	return render(request,
				 'account/edit.html', 
				 {'user_form': user_form})

# Обработчик регистраций
def register(request):
	if request.method == 'POST':
		user_form = UserRedistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(
					 user_form.cleaned_data['password'])
			new_user.save()
			return render(request, 'account/register_done.html',
									{'new_user': new_user})
	else:
		user_form = UserRedistrationForm()

	return render(request, 'account/register.html',
							{'user_form': user_form})
