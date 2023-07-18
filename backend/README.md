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


### Теги
<details>
<summary><strong>GET</strong> [/api/tags/] - Cписок тегов</summary>
<pre>
[
  {
    "id": 0,
    "name": "Завтрак",
    "color": "#E26C2D",
    "slug": "breakfast"
  }
]
</pre>
</details>

<details>
<summary><strong>GET</strong> [/api/tags/{id}] - Получение тега</summary>
<pre>
{
  "id": 0,
  "name": "Завтрак",
  "color": "#E26C2D",
  "slug": "breakfast"
}
</pre>
</details>



### Рецепты
<details>
<summary><strong>GET</strong> [/api/recipes/] - Список рецептов</summary>
<pre>
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
</pre>
</details>

<details>
<summary><strong>POST</strong> [/api/recipes/] - Создание рецепта</summary>
<pre>
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
</pre>
</details>

<details>
<summary><strong>GET</strong> [/api/recipes/{id}] - Получение рецепта</summary>
<pre>
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
</pre>
</details>

<details>
<summary><strong>PATCH</strong> [/api/recipes/{id}] - Обновление рецепта</summary>
<pre>
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
</pre>
</details>

**DELETE** [/api/recipes/{id}] - Удаление рецепта



### Список покупок
**GET** [/api/recipes/download_shopping_cart/] - Скачать список покупок

<details>
<summary><strong>POST</strong> [/api/recipes/{id}/shopping_cart/] - Добавить рецепт в список покупок</summary>
<pre>
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}
</pre>
</details>

**DELETE** [/api/recipes/{id}/shopping_cart/] - Удалить рецепт из списка покупок



### Избранное
<details>
<summary><strong>POST</strong> [/api/recipes/{id}/favorite/] - Добавить рецепт в избранное</summary>
<pre>
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}
</pre>
</details>

**DELETE** [/api/recipes/{id}/favorite/] - Удалить рецепт из избранного


### Подписки
<details>
<summary><strong>GET</strong> [/api/users/subscriptions/] - Мои подписки</summary>
<pre>
{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/subscriptions/?page=4",
  "previous": "http://foodgram.example.org/api/users/subscriptions/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": true,
      "recipes": [
        {
          "id": 0,
          "name": "string",
          "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
          "cooking_time": 1
        }
      ],
      "recipes_count": 0
    }
  ]
}
</pre>
</details>

<details>
<summary><strong>POST</strong> [/api/users/{id}/subscribe/] - Подписаться на пользователя</summary>
<pre>
{
  "email": "user@example.com",
  "id": 0,
  "username": "string",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "is_subscribed": true,
  "recipes": [
    {
      "id": 0,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "cooking_time": 1
    }
  ],
  "recipes_count": 0
}
</pre>
</details>

**DELETE** [/api/users/{id}/subscribe/] - Отписаться от пользователя



### Ингредиенты
<details>
<summary><strong>GET</strong> [/api/ingredients/] - Список ингредиентов</summary>
<pre>
[
  {
    "id": 0,
    "name": "Капуста",
    "measurement_unit": "кг"
  }
]
</pre>
</details>

<details>
<summary><strong>GET</strong> [/api/ingredients/{id}] - Получение ингредиента</summary>
<pre>
{
  "id": 0,
  "name": "Капуста",
  "measurement_unit": "кг"
}
</pre>
</details>


### Документация OpenAPI
Подробная документация по проекту c использованием спецификации OpenAPI доступна по адресу http://127.0.0.1:8000/redoc/

### Автор.
Выполнено **Зюзиным Андреем** в качестве проектного задания Яндекс.Практикум








