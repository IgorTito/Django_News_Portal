
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('adm/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('posts/', include('PortalNews.urls')),
    path('', include('PortalNews.urls')),
    path('accounts/', include('allauth.urls')),
]
