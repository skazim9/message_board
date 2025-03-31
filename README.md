# Доска объявлений

Проект доска объявлений, разработанный с использованием Django REST Framework. Позволяет пользователям создавать объявления, оставлять отзывы и управлять своим контентом.

## Функциональность

- Регистрация и авторизация пользователей
- Создание, редактирование и удаление объявлений
- Добавление отзывов к объявлениям
- Поиск объявлений по названию
- Пагинация объявлений (4 объявления на страницу)
- Разграничение прав доступа (администраторы, авторы, анонимные пользователи)
- Сброс пароля через email

## Технологии

- Python 3.8+
- Django 5.0.2
- Django REST Framework 3.14.0
- PostgreSQL
- JWT-аутентификация
- Django Filter
- Pillow (для работы с изображениями)

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/skazim9/message_board
cd message_board
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env в корневой директории проекта и добавьте необходимые переменные окружения:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

5. Примените миграции:
```bash
python manage.py migrate
```

6. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

7. Запустите сервер разработки:
```bash
python manage.py runserver
```

## API Endpoints

### Объявления

- `GET /ads/` - список всех объявлений
- `POST /ads/` - создание нового объявления
- `GET /ads/{id}/` - детали объявления
- `PUT /ads/{id}/` - обновление объявления
- `DELETE /ads/{id}/` - удаление объявления

### Отзывы

- `GET /ads/{id}/reviews/` - список отзывов к объявлению
- `POST /ads/{id}/reviews/` - создание отзыва
- `PUT /ads/{id}/reviews/{id}/` - обновление отзыва
- `DELETE /ads/{id}/reviews/{id}/` - удаление отзыва

### Пользователи

- `POST /users/reset_password/` - запрос на сброс пароля
- `POST /users/reset_password_confirm/` - подтверждение сброса пароля

## Фильтрация и поиск

### Объявления

- Поиск по названию: `GET /ads/?title=телефон`
- Сортировка по цене: `GET /ads/?ordering=-price`
- Сортировка по дате: `GET /ads/?ordering=-created_at`
- Пагинация: `GET /ads/?page=2`

## Права доступа

- Анонимные пользователи могут только просматривать объявления и отзывы
- Авторизованные пользователи могут создавать объявления и отзывы
- Авторы могут редактировать и удалять свои объявления и отзывы
- Администраторы имеют полный доступ ко всем операциям

## Разработка

### Структура проекта

```
message_board/
├── board/              # Приложение для объявлений
│   ├── filters.py      # Фильтры для объявлений
│   ├── models.py       # Модели данных
│   ├── views.py        # Представления
│   └── urls.py         # URL-маршруты
├── users/              # Приложение для пользователей
│   ├── models.py       # Модель пользователя
│   └── views.py        # Представления
├── message_board/      # Основной проект
│   ├── settings.py     # Настройки проекта
│   └── urls.py         # Основные URL-маршруты
└── requirements.txt    # Зависимости проекта
```

## Лицензия

MIT 