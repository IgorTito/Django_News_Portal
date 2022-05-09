import datetime

from celery import shared_task
import time

from django.contrib.auth.models import User
from django.core.mail import send_mail

from .models import Category, Post


@shared_task
def every_create_post(instance):
    print("*******************************************")
    for pc in Post.objects.get(pk=instance).postCategory.all():
        subs = Category.objects.filter(theme=pc).values("subscribers")
        for sub in subs:
            send_mail(
                subject=f"{Post.objects.get(pk=instance).name_of_article_or_news}",
                message=f"Здравствуйте, {User.objects.get(pk=sub['subscribers']).username}. "
                        f"Вы подписаны на рассылку с сайта PortalNews \n"
                        f"cообщаем Вам, что вышел новый пост в категории, на которую вы подписаны\n"
                        f"Наименование поста - {Post.objects.get(pk=instance).name_of_article_or_news} \n"
                        f"Ознакомительный отрывок - {Post.objects.get(pk=instance).text_of_article_or_news[:20]} \n"
                        f"Если хотите прочитать полный текст, перейдите по ссылке http://127.0.0.1:8000/posts/{instance}",
                from_email='hayabusaigor@yandex.ru',
                recipient_list=[User.objects.get(pk=sub['subscribers']).email]
            )

@shared_task
def every_week():
    delta = datetime.timedelta(seconds=10)
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