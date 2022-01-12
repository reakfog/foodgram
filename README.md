![example workflow](https://github.com/reakfog/foodgram/actions/workflows/main.yml/badge.svg)

# Foodgram

Проект: [Foodgram](http://www.johnperchun.com/)
Автор: [Перчун Евгений](https://github.com/reakfog)

Дипломный проект Яндек Практикум факультета "Бэкенд разработки".

## Содержание
1. [Описание](#description)
2. [Запуск проекта](#launch)
3. [Дополнитольно](#additional)

## <a name='description'>Описание</a>
Проект **Foodgram** создан для создания и хранения рецептов оналайн.
Пользователи могут делиться своими рецептами и составлять списки покупок.

## <a name='launch'>Запуск проекта</a>
Чтобы развернуть проект необходимо выполнить следующие действия (у Вас уже должен быть установлен Docker):

* создайте `.env` файл
  * touch backend/.env
  * echo SECRET_KEY=`ваш секретный ключ` >> .env
  * echo DEBUG=0 >> .env
  * echo ALLOWED_HOSTS=* >> .env
  * echo LANGUAGE_CODE=en >> .env
  * echo TIME_ZONE=Europe/Moscow >> .env
  * echo DB_ENGINE=django.db.backends.postgresql >> .env
  * echo DB_NAME=postgres >> .env
  * echo POSTGRES_USER=postgres >> .env
  * echo POSTGRES_PASSWORD=postgres >> .env
  * echo DB_HOST=db >> .env
  * echo DB_PORT=5432 >> .env
* для запуска выполните команды:
  * `cd infra/`
  * `docker-compose -f docker-compose.local.yml up -d --build` - локальный запуск
  * `docker-compose up -d --build` - запуск на сервере
  * `docker-compose exec backend python manage.py migrate --noinput`
  * `docker-compose exec backend python manage.py createsuperuser`
  * `docker-compose exec backend python manage.py collectstatic --no-input`
* при желании можно загруить тестовые данные в базу данных:
  * `docker-compose exec backend python manage.py load_data`

Проект будет доступен по адресу http://localhost/ при локальной разработке.
Готовый проект можно найти на сайте http://johnperchun.com

## <a name='additional'>Дополнитольно</a>
Также есть тестовый админитратор для обзора админ панели.
Логин: test_user
Пароль: 123456789_test
Чтобы войти, перейдите по ссылке http://johnperchun.com/admin
