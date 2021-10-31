import os
from celery import Celery

# Задаем переменную окружения, содержащую названия файла настроек нашего проекта.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()




