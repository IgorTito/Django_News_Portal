from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
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
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='account/signup.html'), name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('signin/', IndexView.as_view(template_name='account/signin.html'), name="signin"),
    path('category/', CategoryList.as_view(), name='category'),
    path('subscribe/<int:pk>', add_sub, name='subscribe'),


]
