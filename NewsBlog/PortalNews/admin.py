from django.contrib import admin
from .models import Author, Post, Category, PostCategory




# создаём новый класс для представления товаров в админке
class PostCategoryAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = [field.name for field in PostCategory._meta.get_fields()] # генерируем список имён всех полей для более красивого отображения
    list_filter = ("id", "interCategory") # добавляем примитивные фильтры в нашу админку
    search_fields = ('interCategory', "interPost")  # тут всё очень похоже на фильтры из запросов в базу

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory, PostCategoryAdmin)