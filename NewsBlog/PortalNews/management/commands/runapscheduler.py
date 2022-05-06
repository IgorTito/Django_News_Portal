import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
import datetime
from ...models import Post, Category, User

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    delta = datetime.timedelta(weeks=1)
    today = datetime.date.today()
    notify = Post.objects.filter(date_of_create__gt=today-delta).values("postCategory", "name_of_article_or_news", "pk")
    print(notify)

    for category in Category.objects.values("theme", "pk"):

        category_list = []
        for post in notify:
            if post['postCategory'] == category['pk']:
                category_list.append(post['pk'])

        if not category_list == []:
            for user in User.objects.values("subscribers", "username", "email"):

                if user["subscribers"] == category["pk"]:

                    send_mail(
                        subject=f"Вас приветствует PortalNews!",
                        message=f"Салют, {user['username']}! "
                                f"Список постов за прошедшую неделю в категории - {category['theme']} уже готов!\n"
                                f"Ссылка на посты: http://127.0.0.1:8000/posts/search/?name_of_article_or_news__icontains=&category=&rating_of_article_or_news__gt=&postCategory={category['pk']}&date_of_create={today-delta} \n"
                                f"отсортируйте по необходимым тегам \n"
                                f"{today-delta}",
                        from_email='hayabusaigor@yandex.ru',
                        recipient_list=[user['email']],
                    )




# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(week="*/1"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")