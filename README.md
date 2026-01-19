![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=AlexanKoh&repo=Wallet_API&layout=compact&theme=radical&hide_border=true)

# Wallet API

REST API для управления кошельками пользователей с поддержкой конкурентных операций.

## Функциональность

### Основные эндпоинты:

1. **Создание кошелька**
   ```
   POST /api/v1/wallets
   ```
   Возвращает UUID созданного кошелька с начальным балансом 0.

2. **Получение баланса**
   ```
   GET /api/v1/wallets/{wallet_id}
   ```
   Возвращает текущий баланс указанного кошелька.

3. **Изменение баланса**
   ```
   POST /api/v1/wallets/{wallet_id}/operation
   ```
   Проводит операцию пополнения (DEPOSIT) или списания (WITHDRAW).
   
   **Тело запроса:**
   ```json
   {
     "operation_type": "DEPOSIT" or "WITHDRAW",
     "amount": 1000.50
   }
   ```

## Технологии

- **FastAPI** - асинхронный веб-фреймворк
- **SQLAlchemy** + **asyncpg** - асинхронная работа с БД
- **PostgreSQL** - база данных
- **Alembic** - миграции базы данных
- **Docker** + **Docker Compose** - контейнеризация

## Запуск приложения

### Требования:
- Docker
- Docker Compose

### Запуск:

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd wallet

# Запустите приложение
docker-compose up
```

Приложение будет доступно по адресу: **http://localhost:8000**

### Остановка:
```bash
docker-compose down
```

## Документация API

После запуска доступна интерактивная документация:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Особенности реализации

1. **Конкурентная безопасность** - использование `SELECT FOR UPDATE` для предотвращения race condition
2. **Асинхронность** - все операции выполняются асинхронно
3. **Автоматические миграции** - миграции БД применяются при старте приложения
4. **Валидация данных** - проверка типов операций и сумм
5. **Обработка ошибок** - корректные HTTP-статусы и сообщения об ошибках

## Тестирование

```bash
# Запуск тестов
docker-compose exec app pytest tests/
```

## Структура проекта

```
app/
├── main.py          # Точка входа FastAPI
├── models.py        # Модели SQLAlchemy
├── schemas.py       # Pydantic схемы
├── crud.py          # Бизнес-логика
├── database.py      # Настройка БД
├── routers.py       # Эндпоинты API
└── ...
migrations/          # Миграции Alembic
tests/               # Тесты
docker-compose.yml   # Конфигурация Docker
Dockerfile          # Образ приложения
```

## Конфигурация

Настройки задаются через переменные окружения (`.env`):
- `POSTGRES_USER` - пользователь БД
- `POSTGRES_PASSWORD` - пароль БД
- `POSTGRES_DB` - имя базы данных
- `POSTGRES_HOST` - хост БД
- `POSTGRES_PORT` - порт БД
