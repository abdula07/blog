from celery import Celery
from django.core.mail import send_mail
from .models import Comment
from mysite.celery import app

@app.task
def comment_add(comment_id):
	comment = Comment.objects.get(id=comment_id)
	subject = 'Comment in {}'.format(comment.id)
	message = ""
	mail_sent = send_mail(subject, message,
						  'kajnazarov06@mail.ru',
						  [comment.email])
	return mail_sent
