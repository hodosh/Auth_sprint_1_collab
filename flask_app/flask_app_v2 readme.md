# Flask app v2

**Требования к окружению**
 - Запущенный PostgreSQL 


**Запуск**

`flask run` в консоли в папке src


**Создание миграции**

`flask db migrate -m "comment"` Создает новую миграцию


Применение миграции
`flask db upgrade` Применяет миграцию к базе данных                   