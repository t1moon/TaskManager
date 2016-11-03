#Task Manager

Запускаем из корня программы где лежит manage.py
Используемая версия python = 2.7

Для начала нужно поменять коннектор к базе данных mysql в settings.py на свою
Далее создаём базу данных db_task:
в mysql под рутом:
CREATE DATABASE `db_task` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;

#Выполняем действия для наполнение её таблицами и данными:

Для создания миграций БД:
python manage.py makemigrations

eсли будут ошибки, то удалить все миграции в папке mirgations

Для применения миграций после создания БД
python manage.py migrate

Заполняем фэйковыми данными
python manage.py fill       (создаём пользователя "timur@mail.ru" "12345" и даём ему задачи"

Если нужно, можно сбросить данные из таблицы
python manage.py reset

Для пересоздания базы данных
python manage.py resetdb

#Начало работы
перекидывает в login если не залогинен
так как после fill у нас есть timur@mail.ru, то заходим под него чтобы глянуть задачи

# Что не работает
(пока не работает верификация регистрации по email и теги пока без ajax)

