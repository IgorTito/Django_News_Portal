from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.validators import MinValueValidator
from django.urls import reverse

# create models



class Author(models.Model):
    author_name = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    # Метод update_rating() модели Author, который обновляет рейтинг пользователя, переданный в аргумент этого
    # метода. Он состоит из    следующего:    суммарный    рейтинг    каждой    статьи    автора    умножается
    # на    3;    суммарный    рейтинг    всех    комментариев    автора;    суммарный    рейтинг    всех    комментариев
    # к    статьям    автора.
    def update_rating(self):
        updateRatingPost = self.post_set.aggregate(rating_P=Sum("rating_of_article_or_news"))
        p_rat = 0
        p_rat += updateRatingPost.get("rating_P")

        updateRatingComment = self.author_name.comment_set.aggregate(rating_C=Sum("commentRating"))
        c_rat = 0
        c_rat += updateRatingComment.get("rating_C")

        self.rating = (c_rat + p_rat) * 3
        self.save()
    def __str__(self):
        return f"{self.author_name}"


# Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.).
# Имеет единственное поле: название категории. Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True).
class Category(models.Model):
    theme = models.CharField(max_length=100, unique=True)


# Эта модель должна содержать в себе статьи и новости, которые создают пользователи. Каждый объект может иметь одну или несколько категорий.
# Соответственно, модель должна включать следующие поля:
# связь «один ко многим» с моделью Author;
# поле с выбором — «статья» или «новость»;
# автоматически добавляемая дата и время создания;
# связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
# заголовок статьи/новости;
# текст статьи/новости;
# рейтинг статьи/новости.
class Post(models.Model):
    name = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Имя автора")
    ARTICLE = "AR"
    NEWS = "NE"
    CATEGORY = (
        (ARTICLE, "Статья"),
        (NEWS, "Новость")
    )
    category = models.CharField(max_length=2, choices=CATEGORY, default=NEWS, verbose_name="Категория")
    date_of_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    name_of_article_or_news = models.CharField(max_length=128, verbose_name="Заголовок")
    text_of_article_or_news = models.TextField(verbose_name="Текст")
    rating_of_article_or_news = models.SmallIntegerField(default=0, verbose_name="Рейтинг")
    postCategory = models.ManyToManyField(Category, through="PostCategory")

    def __str__(self):
        return f"{self.name_of_article_or_news}"
    def get_absolute_url(self):
        return reverse('one_post', args=[str(self.id)])
    class Meta():
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def like(self):
        self.rating_of_article_or_news += 1
        self.save()

    def dislike(self):
        self.rating_of_article_or_news -= 1
        self.save()

    def preview(self):
        return f"{(self.text_of_article_or_news)[0:20]}{'...'}"



# Промежуточная модель для связи «многие ко многим»:
# связь «один ко многим» с моделью Post;
# связь «один ко многим» с моделью Category.
class PostCategory(models.Model):
    interPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    interCategory = models.ForeignKey(Category, on_delete=models.CASCADE)


# Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
# Модель будет иметь следующие поля:
# связь «один ко многим» с моделью Post;
# связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
# текст комментария;
# дата и время создания комментария;
# рейтинг комментария.
class Comment(models.Model):
    comment_under_art_or_news = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    commentDateTime = models.DateTimeField(auto_now_add=True)
    commentRating = models.SmallIntegerField(default=0)

    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()
