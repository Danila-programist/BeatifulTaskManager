### Бэкенд

Документация по папкам, файлам и функциональности проекта: \

Папки и файлы: 
- `alembic` - папка с миграциями для связи между БД и sqlalchemy
- `app` - основное приложение со всей бизнес-логикой
- `img` - картинки
- `tests` - тестирование юнит-тестами и интеграционными тестами папки `app`
- `pylintrc` - первичные настройки для pylint
- `alembic.ini` - файл инициализации и подключения по DSN макета БД 
- `Dockerfile` - докер-файл для образа приложения
- `main.py` - файл с запуском приложения
- `poetry.toml` - библеотеки для python и определенные конфигурации для poetry
- `pytest.int` - первичные настройки для pytest

Пройдемся по внутренним пакетам приложения `app`:

- `api` - взаимодействие с API со встроенными схемами pydantic и реализацией эндпоинтов авторизации, задач и аналитики
- `auth` - пакет авторизации и аутентификации с использованием JWT-токенов
- `core` - пакет ядра приложения, которое подтягивает с помощью pydantic-settings с файла .env переменные 
- `db` - инициализационный пакет sqlalchemy с базой данных 
- `models` - пакет с таблицами для базы данных sqlalchemy
- `services` - пакет с сервисами, оперириющие с моделями sqlalchemy
- `utils` - пакет утилит и вспомогательных модулей

### Описание эндпоинтов API

## Аутентификация (/api/v1/auth)


🔐 Регистрация нового пользователя

- Метод: POST /api/v1/auth/register
- Описание: Создание нового аккаунта пользователя
- Тело запроса:

```json
{
  "username": "string (3-32 символа)",
  "email": "string (email)",
  "password": "string (мин. 8 символов)",
  "first_name": "string",
  "last_name": "string"
}
```

- Успешный ответ: 200 OK

```json
{"Message": "User was added to the database"}
```

- Ошибки: 404 Not Found - если пользователь уже существует

🔑 Авторизация пользователя

- Метод: POST /api/v1/auth/login
- Описание: Вход в систему, установка JWT-токена в cookies
- Тело запроса:

```json
{
  "username": "string",
  "password": "string"
}
```

- Успешный ответ: 200 OK

```json
{"Message": "User was authorized"}
```

- Cookie: Устанавливает task_manager_token (httpOnly)
- Ошибки: 404 Not Found - неверные учетные данные

🚪 Выход из системы

- Метод: POST /api/v1/auth/logout

- Описание: Выход пользователя, удаление токена

- Успешный ответ: 200 OK

```json
{"Message": "Successfully logged out"}
```

- Cookie: Удаляет task_manager_token

## Управление задачами (/api/v1/tasks)

Все endpoints требуют *аутентификации*

📋 Получение всех задач пользователя

- Метод: GET /api/v1/tasks
- Описание: Возвращает список всех активных задач текущего пользователя
- Успешный ответ: 200 OK

```json
[
  {
    "task_id": "integer",
    "title": "string (макс. 256 символов)",
    "description": "string | null",
    "status": "pending | in_progress | completed",
    "created_at": "datetime",
    "updated_at": "datetime", 
    "is_active": "boolean",
    "user_id": "UUID"
  }
  ...
]
```
- Сортировка: По дате создания (новые сначала)

➕ Создание новой задачи

- Метод: POST /api/v1/tasks
- Описание: Создание новой задачи для текущего пользователя
- Тело запроса:

```json
{
  "title": "string (обязательно, макс. 256 символов)",
  "description": "string | null",
  "status": "pending | in_progress | completed"
}
```
- Успешный ответ: 200 OK

```json
{"message": "Task was added"}
```
- Ошибки: 400 Bad Request - ошибка создания задачи

👀 Получение задачи по ID
- Метод: GET /api/v1/tasks/{task_id}

- Описание: Получение конкретной задачи пользователя

- Параметры: task_id - integer ID задачи

- Успешный ответ: 200 OK 

- Ошибки: 404 Not Found - задача не найдена или нет доступа


✏️ Обновление задачи
- Метод: PUT /api/v1/tasks/{task_id}

- Описание: Полное обновление данных задачи

- Параметры: task_id - integer ID задачи

- Тело запроса: 

```json
{
  "title": "string (обязательно, макс. 256 символов)",
  "description": "string | null",
  "status": "pending | in_progress | completed"
}
```

- Успешный ответ: 200 OK - обновленный объект задачи

- Ошибки: 404 Not Found - задача не найдена или нет доступа

🗑️ Удаление задачи
- Метод: DELETE /api/v1/tasks/{task_id}

- Описание: Мягкое удаление задачи (is_active = false)

- Параметры: task_id - integer ID задачи

- Успешный ответ: 200 OK


- Ошибки: 404 Not Found - задача не найдена или нет доступа


## Аналитика (/api/v1/analytics)

📊 Получение аналитики

- Метод: GET /api/v1/analytics

- Описание: Получение основной информации о задачах пользователя

- Успешный ответ: 200 OK


```json

{
  "user_info": {
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string"
  },
  "tasks_overview": {
    "total_tasks": "integer",
    "active_tasks": "integer",
    "completed_tasks": "integer",
    "completion_rate": "float (0-1)"
  },
  "productivity_metrics": {
    "tasks_created_today": "integer",
    "tasks_completed_today": "integer",
    "tasks_created_this_week": "integer",
    "tasks_completed_this_week": "integer",
  },
  "recent_activity": {
    "last_task_created": "datetime | null",
    "last_task_completed": "datetime | null",
    "most_active_day": "string"
  },
  "tasks_created_by_weekday": {
    "monday": "integer",
    "tuesday": "integer",
    // ... все дни недели
  }
}

```

### Схематичное представление реализации бэкенда

![alt text](/backend/img/image.png)