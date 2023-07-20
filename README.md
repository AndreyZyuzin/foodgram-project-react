### Foodgram
Foodgram - сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 

### Стэк Технологий.
- Python 3.10
- Django 3.2
- Django rest framework 3.14
- Postgersql
- React
- nginx
- gunicorn
- Docker


### Как установить.
На сервере устанавливается директория Foodgram.
В которой копируется файл docker-compose.production.yml.
Так же добавляется файл .env, в котором должны быть
```
POSTGRES_DB=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...

DB_NAME=...
DB_HOST=...
DB_PORT=...

SECRET_KEY=...
DEBUG=...
ALLOWED_HOSTS=<ip>,127.0.0.1,localhost,<domain>

OUT_PORT_FOODGRAM=...
```

Для запуска следует выйти в папку foodgram
```
make install_and_run
```

Для создания аккаунта админа, следует выполнить
```
make create_superuser
```

наполнение базы данных ингредиентов:
```
make load_ingredients
```

### Данные сервера
[foodgram](https://xn--80aciep1ase.site/ "Оснавная ссылка")  
или  
[foodgram](http://51.250.109.52:7000/ "по ip")  
  
Панель администрирования:
[админка](https://xn--80aciep1ase.site/admin/)  
логин: admin  
пароль: admin  

### Другие приложения
[Taski](http://51.250.109.52:8000/)  
[kittygram](http://51.250.109.52:9000/)


### Автор.
Выполнено **Зюзиным Андреем** в качестве проектного задания Яндекс.Практикум
