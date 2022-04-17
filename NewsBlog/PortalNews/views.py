from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post
from .filters import PostFilter


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_of_create'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 5


    def get_queryset(self):
        queryset = super().get_queryset()
       # Используем наш класс фильтрации.
       # self.request.GET содержит объект QueryDict, который мы рассматривали
       # Сохраняем нашу фильтрацию в объекте класса,
       # чтобы потом добавить в контекст и использовать в шаблоне
        self.filterset = PostFilter(self.request.GET, queryset)
       # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['filterset'] = self.filterset
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        # Добавляем в контекст объект фильтрации.

        return context


class OnePost(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


# создание новости
class CreateNews(CreateView):
    # Указываем форму
    form_class = PostForm
    #  Указываем модель
    model = Post
    # шаблон, в котором используем форму.
    template_name = 'news_post_create.html'
    def form_valid(self, form): # разделяем новости и статьи
        post = form.save(commit=True)
        post.category = "NE"
        return super().form_valid(form)
# создание статьи
class CreateArticles(CreateView):
    # Указываем форму
    form_class = PostForm
    #  Указываем модель
    model = Post
    # шаблон, в котором используем форму.
    template_name = 'articles_post_create.html'
    def form_valid(self, form):
        post = form.save(commit=True)
        post.category = "AR"
        return super().form_valid(form)

# изменение новости
class NewsUpdatePost(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "news_post_update.html"

    # если пост был создан как новость, то изменения будут в "новости", если пользователь вручную прописывает путь
    # например /articles/ID/update, то получаем ошибку
    def form_valid(self, form):
        news = form.save(commit=True)
        if news.category == "NE":
            return super().form_valid(form)
# изменение статьи
class ArticlesUpdatePost(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "articles_post_update.html"
    def form_valid(self, form):         # если пост был создан как статья, то изменения будут в "статьe"
        ar = form.save(commit=True)
        if ar.category == "AR":
            return super().form_valid(form)

class NewsDeletePost(DeleteView):
    model = Post
    template_name = "news_post_delete.html"
    success_url = reverse_lazy('posts_list')  # куда направляем после удаления

class ArticlesDeletePost(DeleteView):
    model = Post
    success_url = reverse_lazy('posts_list') #куда направляем после удаления
    template_name = "articles_post_delete.html"


class SearchPost(ListView):
    model = Post
    ordering = ["-date_of_create"]
    template_name = "post_search.html"
    context_object_name = 'find'

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['find'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        # Добавляем в контекст объект фильтрации.
        return context


