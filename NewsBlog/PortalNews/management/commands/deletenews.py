from django.core.management.base import BaseCommand, CommandError
from PortalNews.models import Post, Category

class Command(BaseCommand):
    help = "Удаляет все новости в категории"

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы действительно хотите удалить все новости в категории {options["category"]}? yes/no  ')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))

        try:
            category_del = Category.objects.get(theme=options['category'])
            print(category_del)
            Post.objects.filter(postCategory = category_del).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Успешно удалены все новости из категории {category_del.theme}'))  # в случае неправильного подтверждения говорим, что в доступе отказано
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Не найдена категория - {category_del.theme}'))