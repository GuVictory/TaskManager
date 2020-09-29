# Task manager API

Основный url для работы с API: http://127.0.0.1:8000/api/


##Работа с пользвателем

#### Регистрация:
* Url: /users/
* Method: POST
* Request body:
```json
{
  "username": "username",
  "password": "password"
}
```
* Response status 201 and body:
```json
{
  "id": "id",
  "username": "username"
}
```
* Response status 400 and body:
```json
{
  "username":["A user with that username already exists."]
}
```
***
#### Авторизация
* Url: /login/
* Method: POST
* Request body:
```json
{
  "username": "username",
  "password": "password"
}
```
* Response status 200 and body:
```json
{
  "token": "hello_token_example",
}
```
* Response status 400 and body:
```json
{
  "non_field_errors":["Unable to log in with provided credentials."]
}
```