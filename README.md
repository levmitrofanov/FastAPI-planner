# Planner API (ветка planner-nosql)

REST API планировщика событий и мониторинга сетевых узлов с подключением к нереляционной СУБД MongoDB через асинхронный ODM Beanie.

## Стек технологий
- **Язык программирования:** Python 3.11
- **Фреймворк:** FastAPI 0.115.0
- **ASGI-сервер:** Uvicorn 0.30.6
- **СУБД / ODM:** MongoDB / Beanie ODM (Motor, PyMongo)
- **Валидация данных:** Pydantic v2 / Pydantic Settings

## Архитектура проекта
- `database/connection.py` — класс Settings для чтения DATABASE_URL из .env и универсальный класс Database для CRUD-операций над документами Beanie.
- `models/events.py` — модель документа Event и схема обновления EventUpdate.
- `models/users.py` — модель документа User (с ссылками Link[Event]) и схема UserSignIn.
- `models/nodes.py` — модель документа NetworkNode и схема обновления NetworkNodeUpdate (персональная тема: «Управление сетевыми узлами»).
- `routes/events.py` — эндпоинты CRUD для событий (/event/).
- `routes/users.py` — регистрация (/user/signup) и аутентификация (/user/signin).
- `routes/nodes.py` — эндпоинты CRUD для сетевых узлов (/node/).
- `main.py` — точка входа, подключение роутеров и инициализация соединения с MongoDB в обработчике startup.

## Инструкция по запуску
1. Активировать виртуальное окружение:
   ```bash
   source venv/Scripts/activate
   ```
2. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустить сервер MongoDB:
   ```bash
   mongod --dbpath store
   ```
4. Запустить приложение FastAPI:
   ```bash
   python main.py
   ```
5. Интерактивная документация Swagger UI доступна по адресу: `http://127.0.0.1:8080/docs`.
