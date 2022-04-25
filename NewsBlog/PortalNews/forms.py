from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

from .models import Post, Author


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "name",
            "name_of_article_or_news",
            "text_of_article_or_news",
        ]
    def clean(self):
        cleaned_data = super().clean()
        text_valid = cleaned_data.get("text_of_article_or_news")
        if text_valid is not None and 500 < len(text_valid):
            raise ValidationError({
                "text_of_article_or_news": "Текст статьи превышает 500 символов"
            })
        return cleaned_data


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = {
            "author_name"
        }


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    # first_name = forms.CharField(label="Имя")
    # last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  # 'first_name',
                  # 'last_name',
                  "email",
                  "password1",
                  "password2",)
# добавление в группу при регистрации
    def save(self, commit=True):
        user = super(BaseRegisterForm, self).save()
        main_group = Group.objects.get(name='common')
        main_group.user_set.add(user)
        Author.objects.create(author_name=user)
        return user
