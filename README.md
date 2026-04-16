# 📚 Архив документов

## Быстрый старт

1. Клонируйте репозиторий
2. Создайте виртуальное окружение: `python -m venv venv`
3. Активируйте: `venv\Scripts\activate` (Windows) или `source venv/bin/activate` (Mac/Linux)
4. Установите зависимости: `pip install -r requirements.txt`
5. Скопируйте `.env.example` в `.env`
6. Запустите PostgreSQL: `docker run --name db -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=document_db -p 5432:5432 -d postgres:15`
7. Примените миграции: `python manage.py migrate`
8. Создайте суперпользователя: `python manage.py createsuperuser`
9. Запустите сервер: `python manage.py runserver`

## Доступ

- Главная: http://localhost:8000
- Админка: http://localhost:8000/admin
