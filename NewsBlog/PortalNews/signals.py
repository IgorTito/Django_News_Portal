from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from .models import *
from django.core.mail import send_mail




@receiver(m2m_changed, sender=PostCategory)
def notify_send_mail(instance, **kwargs):


    for pc in instance.postCategory.all():
        subs = Category.objects.filter(theme=pc).values("subscribers")
        for sub in subs:
            send_mail(
                subject=f"{instance.name_of_article_or_news}",
                message=f"Здравствуйте, {User.objects.get(pk=sub['subscribers']).username}. "
                        f"Вы подписаны на рассылку с сайта PortalNews \n"
                        f"cообщаем Вам, что вышел новый пост в категории, на которую вы подписаны\n"
                        f"Наименование поста - {instance.name_of_article_or_news} \n"
                        f"Ознакомительный отрывок - {instance.text_of_article_or_news[:20]} \n"
                        f"Если хотите прочитать полный текст, перейдите по ссылке http://127.0.0.1:8000/posts/{instance.pk}",
                from_email='hayabusaigor@yandex.ru',
                recipient_list=[User.objects.get(pk=sub['subscribers']).email]
            )