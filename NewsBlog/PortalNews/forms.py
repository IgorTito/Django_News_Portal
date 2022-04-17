from django import forms
from django.core.exceptions import ValidationError

from .models import Post

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
