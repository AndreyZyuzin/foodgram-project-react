import os

from fpdf import FPDF
from django.conf import settings


class PDF(FPDF):
    """Создание pdf файла списка ингредиентов для рецептов."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        DIR_SCRIPT_PDF=os.path.join(
            settings.BASE_DIR, 'static', 'assets', 'font')
        self.add_font(
            'open', '', DIR_SCRIPT_PDF + r'/OpenSans-Regular.ttf')
        self.add_font(
            'open', 'i', DIR_SCRIPT_PDF + r'/OpenSans-Italic.ttf')
        self.add_font(
            'open', 'b', DIR_SCRIPT_PDF + r'/OpenSans-Bold.ttf')
        self.add_font(
            'open', 'bi',
            DIR_SCRIPT_PDF + r'/OpenSans-BoldItalic.ttf')
        
    def header(self):
        self.set_font("open", "B", 15)
        self.cell(80)
        self.cell(30, 10,
                  "Foodgram - Обмен рецептов",
                  border=0,
                  align="C",
                  link='https://ya.ru')
        self.ln(20)

    def print_body(self, data):
        self.set_font("open", "", 18)
        self.cell(0, 6,
                  txt='Список ингредиентов рецептов:',
                  align="L",
                  new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        self.set_font("open", size=14)
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

    def creaete_list_ingredients(self, data, namePDF=None):
        self.add_page()
        self.print_body(data)
        return self.output(namePDF) if namePDF else self.output()


if __name__== '__main__':
    name = 'Рецепт 1'
    data = [{'name': 'алкоголь', 'unit': 'стакан', 'amount': 1},
            {'name': 'айран', 'unit': 'г', 'amount': 1},
            {'name': 'аджика зеленая', 'unit': 'г', 'amount': 10}]

    pdf = PDF().creaete_list_ingredients(data)
    print(pdf)
