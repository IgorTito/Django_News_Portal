from django.urls import path

from .views import PostList, OnePost

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', OnePost.as_view()),
]
