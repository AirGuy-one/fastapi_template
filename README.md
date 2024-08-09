# FastApi Template

### Запуск шаблона:

1) Создайте файл .env, данные нужные для запуска можно посмотреть в .env.example
2) Примените команду для запуска: ```docker-compose up -d --build```
3) Перейдите в контейнер с ботом, для этого после полного запуска введите следующую команду: ```docker exec -it <название_контейнера> bash```
4) Попав в контейнер введите команду для запуска миграций: ```alembic revision -m "<название миграции>" --autogenerate```
5) Примените миграции: ```alembic upgrade head```

Документация к API доступна по url: http://localhost:80/docs/

### Проведение миграций:
1) После создания модели импортируйте ее в ```__init__.py```, который находится в каталоге ```models```
2) Перейдите в контейнер с ботом, для этого после полного запуска введите следующую команду: ```docker exec -it <название_контейнера> bash```
3) Попав в контейнер введите команду для запуска миграций: ```alembic revision -m "<название миграции>" --autogenerate```, тем самым создав ее.
4) Примените миграции: ```alembic upgrade head```


### Создание суперпользователя для админки:

1) Перейдите в контейнер с ботом, для этого после полного запуска введите следующую команду: ```docker exec -it <название_контейнера> bash```
2) Перейдите директорию ```cd scripts```
3) Введите команду для создания суперпользователя: ```python3 create_super_user.py```

    Админка будет доступна по url: http://localhost:80/admin/login


### Backlog

1) Сделать разделение сервисов.
2) Перейти на async SQLAlchemy.