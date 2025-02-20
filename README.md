# Respondent API

## Описание
Приложение предоставляет API с возможностью расчета процента вхождения второй аудитории в первую, основываясь на среднем весе.


## Особенности

- **Загрузка данных**: Загружает респондентов из CSV-файла в базу данных, если база данных пуста.
- **Работа с базой данных**: Подключение к PostgreSQL с использованием SQLAlchemy.
- **Функциональность API**: API для вычисления процента вхождения второй аудитории в первую, основываясь на среднем весе.

## Стек технологий

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Uvicorn (ASGI-сервер)
- Docker и Docker Compose

## Требования

- Docker

## Запуск с использованием Docker

1. Клонируйте репозиторий и перейдите в папку проекта:

    ```bash
    git clone https://github.com/paulinemnl/respondent-api.git
    cd respondent_api
    ```

2. Запустите команду:

    ```bash
    docker-compose up --build
    ```

2. После успешного запуска приложение будет доступно по адресу [http://localhost:80](http://localhost:80) 
(если в БД изначально не было данных, то необходимо подождать несколько секунд для их загрузки)


## Пример запроса API

`GET /getPercent` – вычисляет процент вхождения второй аудитории в первую, основываясь на среднем весе
- `audience1` – SQL-условие для первой аудитории
- `audience2` – SQL-условие для второй аудитории
- Возвращает процент вхождения второй аудитории в первую, основываясь на среднем весе

### Формирование условий фильтрации

Параметры `audience1` и `audience2` должны быть валидными SQL-условиями


Примеры:
- `Age BETWEEN 18 AND 35`
- `Sex = 1`
- `Date='2021-12-31'::date`


### Пример валидного запроса:
**Пример:**
```bash
  curl -X 'GET' \
  'http://127.0.0.1:80/getPercent?audience1=Age%20BETWEEN%2018%20AND%2035&audience2=Sex%20=%202%20AND%20Age%20>=%2018'
  ```

**Ответ**:
```json
{"percent":0.44}
```

### Валидация параметров запроса
При попытке передачи невалидных SQL-условий API вернет ошибку `422
Unprocessable Entity` с детализацией невалидных токенов. 

### Пример невалидного запроса
**Пример**
```bash
  curl -X 'GET' \
  'http://127.0.0.1:80/getPercent?audience1=Age%20BETWEEN%2018%20AND%2035;%20DROP%20TABLE%20respondents;&audience2=sex=1'
  ```

**Ответ**:
```json
{
    "detail": [
        {
            "type": "unsafe_sql_query",
            "loc": [
                "query",
                "audience1"
            ],
            "msg": "Unsafe tokens found in query",
            "input": "Age BETWEEN 18 AND 35; DROP TABLE respondents;",
            "ctx": {
                "tokens": [
                    ";",
                    "DROP",
                    "TABLE",
                    "respondents"
                ]
            }
        }
    ]
}
```

## Структура проекта
```
respondent_api/  
├── app/  
│   ├── api/  
│   │   ├── endpoints/  
│   │   │   └── respondents.py        # API-эндпоинты для респондентов 
│   ├── core/  
│   │   └── config.py                 # Конфиг для приложения
│   ├── db/  
│   │   ├── base.py                   # Базовая настройка SQLAlchemy
│   │   ├── database.py               # Подключение к базе данных и функции инициализации
│   │   └── models.py                 # Модели данных SQLAlchemy 
│   ├── repositories/  
│   │   └── respondent_repository.py  # Репозиторий для работы с данными респондентов 
│   ├── schemas/  
│   │   ├── query_params.py           # Модели запросов Pydantic
│   │   └── responses.py              # Модели ответов Pydantic
│   ├── scripts/  
│   │   └── load_data.py              # Скрипт для загрузки данных в БД из csv файла
│   ├── services/  
│   │   └── respondent_service.py     # Сервис для работы с респондентами
├── data/  
│   └── data.csv                      # Исходные данные 
├── main.py                           # Точка входа в приложение FastAPI
├── docker-compose.yml                # Конфигурация Docker Compose (поднимает API и БД)
├── Dockerfile                        # Dockerfile для сборки Docker-образа приложения
├── README.md
├── .gitignore
└── requirements.txt
```