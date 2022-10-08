# API для проекта YaMDb
## Спринт 10 — api_yamdb

### Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен.

### Технологии
- Python 3.7
- Django 2.2.19
- Django Rest Framework 3.12.4
- SimpleJWT 4.8.0

### Запуск проекта в dev-режиме
Клонируем проект:
```
git clone https://github.com/AnthonyHol/api_yamdb.git
```

Переходим в папку с проектом и устанавливаем виртуальное окружение:

```
python -m venv venv
```

Активируем виртуальное окружение:
```
source venv/Scripts/activate
```

Устанавливаем зависимости:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

Выполняем миграции:
```
python yatube/manage.py makemigrations
```
```
python yatube/manage.py migrate
```

Создаем суперпользователя:
```
python yatube/manage.py createsuperuser
```

В папку, где находится файл settings.py, добавляем файл .env, куда прописываем секретный ключ следующим образом:
```
SECRET_KEY='Секретный ключ'
```

Запускаем проект:
```
python yatube/manage.py runserver
```

Проект будет доступен по адресу `http://127.0.0.1:8000/`

Переход на админ-панель доступен по адресу `http://127.0.0.1:8000/admin/`

### Пример работы с API

```
С доступом для всех:
GET /api/v1/categories/ — Получение списка всех категорий
GET /api/v1/genres/ — Получение списка всех жанров
GET /api/v1/titles/ — Получение списка всех произведений
GET /api/v1/titles/{title_id}/reviews/ — Получение списка всех отзывов
GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ — Получение списка всех комментариев к отзыву

Только с доступом для администратора:
GET /api/v1/users/ — Получение списка всех пользователей
```

### Пользовательские роли
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django — обладает правами администратора (admin).

Подробная документация по всем URL и запросам предоставлена по адресу `http://127.0.0.1:8000/redoc/`.

Авторы: 
- [Холкин Антон (Python-разработчик + Тимлид)](https://github.com/AnthonyHol/ "Холкин Антон (Python-разработчик + Тимлид)")
- [Леонид Клет (Python-разработчик)](https://github.com/lik-me "Леонид Клет(Python-разработчик)")
- [Денис М. (Python-разработчик)](https://github.com/Eltimccc "Денис М (Python-разработчик)")
