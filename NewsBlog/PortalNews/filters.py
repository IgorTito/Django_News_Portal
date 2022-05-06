import django.forms
from django_filters import FilterSet, DateTimeFilter
from .models import Post

from datetime import datetime
# Создаем свой набор фильтров для модели.
# FilterSet, который мы наследуем
class PostFilter(FilterSet):
    date_of_create = DateTimeFilter(lookup_expr="gte", widget=django.forms.DateInput(attrs={"type": "date"}))
    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           "name_of_article_or_news": ["icontains"],
           # поиск по типу
           "category": ["exact"],
           # поиск по рейтингу
           "rating_of_article_or_news": ["gt"],
           # по категории
           "postCategory": ["exact"],
       }