# Социальная сеть для публикации личных дневников
## Спринт 10 — api_yamdb

### Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен.

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

Переход на документацию проекта `http://127.0.0.1:8000/redoc/`

Авторы: 
- [Холкин Антон (Python-разработчик + Тимлид)](https://github.com/AnthonyHol/ "Холкин Антон (Python-разработчик + Тимлид)")
- [Леонид Клет(Python-разработчик)](https://github.com/lik-me "Леонид Клет(Python-разработчик)")
- [Денис М (Python-разработчик)](https://github.com/Eltimccc "Денис М (Python-разработчик)")
