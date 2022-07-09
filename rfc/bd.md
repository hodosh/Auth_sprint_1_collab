# База данных


Схема PostGrees 
![](img/db_scheme.png)

Для хранения **refresh token** используется таблица PG UserHistory.refresh_token.

Для хранения невалидных **accees token** используется Redis.

Валидные **accees token** не храняться на сервере и передаются при каждом обращении кдиента к серверу.