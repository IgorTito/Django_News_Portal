from django.urls import path

from .views import *

urlpatterns = [
    path('', PostList.as_view(), name="posts_list"),
    path('<int:pk>', OnePost.as_view(), name="one_post"),
    path('news/create/', CreateNews.as_view(), name="news_create_post"),
    path('search/', SearchPost.as_view(), name="search_post"),
    path('news/<int:pk>/update/', NewsUpdatePost.as_view(), name="news_update_post"),
    path('news/<int:pk>/delete/', NewsDeletePost.as_view(), name="news_delete_post"),
    path('articles/create/', CreateArticles.as_view(), name="articles_create_post"),
    path('articles/<int:pk>/update/', ArticlesUpdatePost.as_view(), name="articles_update_post"),
    path('articles/<int:pk>/delete/', ArticlesDeletePost.as_view(), name="articles_delete_post"),

]
