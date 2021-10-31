from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns = [
	# Обработчики входа и выхода
	path('login/', auth_views.LoginView.as_view(), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	# Обработчики профиля и редоктирование
	path('', views.my_account, name='my_account' ),
	path('edit/', views.edit_account, name='edit'),
	# Обработчики изменение пароля
	path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
	path('password_change/done', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
	# Обработчики воостановление пароля
	path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
	# Обработчик регистраций пользователей
	path('register/', views.register, name='register')
]