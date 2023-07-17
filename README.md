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

следует войти в эту директорию и запустить несколько команд
```
cd foodgram
sudo docker compose -f docker-compose.production.yml pull
sudo docker compose -f docker-compose.production.yml down
sudo docker compose -f docker-compose.production.yml up -d
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```

наполнение базы данных ингредиентов:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_csv
```

### Автор.
Выполнено **Зюзиным Андреем** в качестве проектного задания Яндекс.Практикум
