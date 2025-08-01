from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_course_update_email(user_email, course_title):
    subject = f'Обновление курса: {course_title}'
    message = f'Курс "{course_title}" был обновлён. Зайдите на сайт, чтобы ознакомиться с изменениями.'
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [user_email])
