## CarPark API на FastAPI

### Стек: `Fastapi`, `PostgreSQL`, `SQLAlchemy`, `Alembic`.

### Схема БД:
![img.png](readme_static%2Fimg.png)

### Основная функциональность:
- `User`:
    - Регистрация юзера через профиль VK: http://127.0.0.1:8080/api/v1/user/vk_auth_start/
    - Получение всех юзеров: http://127.0.0.1:8080/api/v1/user/
    - Получение юзера по id http://127.0.0.1:8080/api/v1/user/1/ # id=1
* Интерактивная документация: http://127.0.0.1:8080/docs


### Инструкции по запуску:
1. `cd <Абсолютный путь к директории CarPark_FastAPI>`
2.  `docker compose -f docker-compose.dev.yml run --name campweek_backend_api --service-ports -d app`
* Полезные команды находятся в `instructions/docker.txt`

### Важные моменты:
Если при сборке образа будет ошибка, то попробуйте удалить "�" в конце `requirements.txt`
