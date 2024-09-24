# PhotoEdger
### Проект выполнен в ахритектурном стиле DDD
Основной домен: Image

#### Использованы паттерны:
  - Observer
  - CQRS
  - Unit of Work
  - MessageBus (Шина сообщений)
  - Репозиторий и др.
  - Dependency Injection

#### Будущие улучшения:
  - Правки тестов

## Описание

PhotoEdger — это приложение для обработки изображений.
Принимает на вход изображение, его название и описание. 

API сохраняет изображение в сыром байтовом формате и отправляет событие в Redis.

Redis, в свою очередь, обрабатывает эти события, создавая черную полосу под изображением и добавляя текст из описания. Обработанное изображение сохраняется в модели визуального представления с маршрутом к сохраненному файлу.

## Зависимости

- Docker
- Docker Compose

### Подготовка переменных окружения
Создать `.env` файл из `.env.example`

```
cp .env.example .env
```

## Запуск проекта

Проект запускается с помощью Makefile:

- Для запуска проекта и Redis-консюмера используйте:
  ```bash
  make up

- Запуск миграций для создания таблиц
- ```bash
  make upgrade
- Для запуска FastAPI:
- ```bash
  make run

- Для остановки проекта:
- ```bash
  make down

- Запуск тестов
- ```bash
  make test

### Управление миграциями
Создание новой миграции
```
docker exec -it backend bash

alembic revision --autogenerate -m "some_comment"
```

Применение миграций:

```
make upgrade

make downgrade
```

Документация типа Swagger:

Доступна по адресу:
http://0.0.0.0:8000/swagger
