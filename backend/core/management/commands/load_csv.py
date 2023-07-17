"""Скрипт наполняющий данные из файлов csv в базу данных.

    Файлы находятся в ../data/*.csv
    Запуск:
        python manage.py load_csv       - добавление в БД
        python manage.py load_csv -u
            - добавление в БД. Найденные элементы будут обновлены
        python manage.py load_csv -d
            - Предваритльено удаляются все таблицы
"""
import csv
import logging
import os

from django.core.management.base import BaseCommand, CommandParser

from foodgram_backend.settings import BASE_DIR

from recipes.models import Ingredient

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    PATH_CSV = os.path.join(BASE_DIR, 'static', 'data')
    FILES_OF_MODELS = {
        'ingredients.csv': (Ingredient, 'name', 'measurement_unit'),
    }

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '-d', '--delete',
            action='store_const', const=True,
            help=('Предварительно удаление всех данных.')
        )

        parser.add_argument(
            '-u', '--update',
            action='store_const', const=True,
            help=('При нахождении элемента и другим содержаниеи обновляется.')
        )

    def handle(self, *args, **options) -> None:
        update = options.get('update')
        delete = options.get('delete')
        name_file = 'ingredients.csv'
        full_name_file = os.path.join(self.PATH_CSV, name_file)

        model, *fields_of_model = self.FILES_OF_MODELS[name_file]
        data = list()
        with open(full_name_file) as file:
            reader = csv.DictReader(
                file,
                fieldnames=fields_of_model
            )
            for numb, row in enumerate(reader):
                try:
                    data.append(dict(**row))
                except TypeError:
                    logger.error(f'В {numb} строке не подходящие данные')
        if delete:
            model.objects.all().delete()
            logger.debug(f'Данные {model.__name__} удалены.')

        for ingredient in data:
            name = ingredient.get('name')
            fields = ('measurement_unit',)
            defaults = {key: ingredient.get(key) for key in fields}
            action = (model.objects.update_or_create if update
                      else model.objects.get_or_create)
            obj, created = action(name=name, defaults=defaults)
