import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsBlog.settings')

app = Celery('NewsBlog')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'posts_every_week': {
        'task': 'PortalNews.tasks.every_week',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

