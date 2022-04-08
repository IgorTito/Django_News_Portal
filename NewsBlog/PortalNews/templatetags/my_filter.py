from django import template

register = template.Library()

WORDS = ["идиот",
         "оболтус",
         "гад",
         "стерва"]


@register.filter()
def cenz(old_words):
    for word in WORDS:
        while word not in old_words.split():
            word = word[:1] + (len(word) * "*")
            for cenz_word in WORDS:
                if cenz_word in old_words:
                    new_words = old_words.replace(cenz_word, word)
                    return new_words
            return old_words
