import os

import yaml
from django.conf import settings
from fpdf import FPDF

file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'pdf_config.yaml'
)
pdf_config = yaml.safe_load(open(file))

DIR_PDF_FONT = 'static/assets/font'


class PDF(FPDF):
    """Создание pdf файла списка ингредиентов для рецептов."""
    conf = pdf_config

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(settings.BASE_DIR)
        dir_script_pdf = os.path.join(settings.BASE_DIR, DIR_PDF_FONT)
        for font in self.conf.get('fonts'):
            self.add_font(
                family=font.get('family'),
                style=font.get('style'),
                fname=os.path.join(dir_script_pdf, font.get('name')),
            )

    def header(self):
        header_ = self.conf.get('header')
        font = header_.get('font')
        self.set_font(
            family=font.get('family'),
            style=font.get('style'),
            size=font.get('size'),
        )
        self.cell(80)
        self.cell(30, 10,
                  "Foodgram - Обмен рецептов",
                  border=0,
                  align="C",
                  link='https://ya.ru')
        self.ln(header_.get('line_break'))

    def print_body(self, data):
        body = self.conf.get('body')
        title_font = body.get('title').get('font')
        self.set_font(
            family=title_font.get('family'),
            style=title_font.get('style'),
            size=title_font.get('size'),
        )
        self.cell(0, 6,
                  txt='Список ингредиентов рецептов:',
                  align="L",
                  new_x="LMARGIN", new_y="NEXT")
        self.ln(body.get('line_break'))

        main_font = body.get('main').get('font')
        self.set_font(
            family=main_font.get('family'),
            style=main_font.get('style'),
            size=main_font.get('size')
        )
        for item in data:
            ingredient_name = item['name']
            unit = item['unit']
            amount = item['amount']
            self.cell(0, 10,
                      f'{ingredient_name[:1].upper()}{ingredient_name[1:]} - '
                      f'{amount} {unit}.',
                      new_x="LMARGIN", new_y="NEXT")

    def footer(self):
        self.set_y(-15)
        self.set_font("open", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def creaete_list_ingredients(self, data, name_pdf=None):
        self.add_page()
        self.print_body(data)
        return self.output(name_pdf) if name_pdf else self.output()
