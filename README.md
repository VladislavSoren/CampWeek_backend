## Backend API для сервиса CampWeek_backend

### Стек: `Fastapi`, `PostgreSQL`, `SQLAlchemy`, `Alembic`.

### Схема БД:
![1_scheme.png](readme_static%2F1_scheme.png)

### Основная функциональность:
- Регистрация юзера через ВК
- Личный кабинет юзера (данные подтягивается из ВК) с возможностью изменения в нём информации
- КРУД для ролей

* Интерактивная документация: http://127.0.0.1:8080/docs


### Инструкции по запуску:
1. `cd <Абсолютный путь к директории CampWeek_backend>`
2.  `docker compose -f docker-compose.dev.yml run --name campweek_backend_api --service-ports -d app`
3. Data migration command `bash data_migration.th`
* Полезные команды находятся в `instructions/docker.txt`

### Важные моменты:
Если при сборке образа будет ошибка, то попробуйте удалить "�" в конце `requirements.txt`

