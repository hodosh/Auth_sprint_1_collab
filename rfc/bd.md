# База данных


Схема PostGrees 
![](img/db_scheme.png)

Для хранения **refresh token** используется таблица PG UserHistory.refresh_token.

Для хранения невалидных **access token** используется Redis.

Валидные **access token** не храняться на сервере и передаются при каждом обращении клиента к серверу.

Схема Payload:
```
{
  "user_id": user_id,
  "email": email,
  "role_id": role_id
}
```