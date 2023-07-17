# Foodgram

## Описание
Foodgram - сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд. 

### Зависимости
Для работоспобности необходимые следующие библиотеки:
>requests 2.31.0  
Django 3.2    
djangorestframework 3.14
psycopg2 2.9.3
PyJWT 2.7
djoser 2.2
django-filter 23.2
fpdf2 2.7.4
Pillow 9.0.0


### Установка
Клонируйте репозиторий коммандой `git@github.com:AndreyZyuzin/foodgram-project-react.git`

Создайте виртуальное окружение   `python3 -m venv venv`

Активируйте виртуальное окружение `source venv/bin/activate`(для Linux и MacOS) `source venv/Scripts/activate` (для Windows)

Установите зависимости `pip install -r requirements.txt`

Выполните миграции `python manage.py makemigration && python manage.py migrate`

Запустите сервер `python manage.py runserver`

### Описание и примеры запросов
### Пользователи
<details>
<summary><strong>GET</strong> [/api/users/] - Список пользователей</summary>
<pre>
{
    "count": 123,
    "next": "http://foodgram.example.org/api/users/?page=4",
    "previous": "http://foodgram.example.org/api/users/?page=2",
    "results": [
        {
            "email": "user@example.com",
            "id": 0,
            "username": "string",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "is_subscribed": false
        }
    ]
}
</pre>
</details>

<details>
<summary><strong>POST</strong> [/api/users/] - Регистрация пользователя</summary>
<pre>
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}
</pre>
</details>

<details>
<summary><strong>GET</strong> [/api/users/{id}/] - Профиль пользователя</summary>
<pre>
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": false
}
</pre>
</details>

<details>
<summary><strong>GET</strong> [/api/users/me/] - Текущий пользователь</summary>
<pre>
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": false
}
</pre>
</details>

<details>
<summary><strong>POST</strong> [/api/users/set_password/] - Изменение пароля</summary>
<pre>
{
  "new_password": "string",
  "current_password": "string"
}
</pre>
</details>

<details>
<summary><strong>POST</strong> [/api/auth/token/login/] - Получить токен авторизации</summary>
<pre>
{
  "password": "string",
  "email": "string"
}
</pre>
</details>

**POST** [/api/auth/token/logout/] - Удаление токена

### Документация OpenAPI
Подробная документация по проекту c использованием спецификации OpenAPI доступна по адресу http://127.0.0.1:8000/redoc/

### Автор.
Выполнено **Зюзиным Андреем** в качестве проектного задания Яндекс.Практикум








