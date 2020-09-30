Task manager API
===

Основный url для работы с API: http://127.0.0.1:8000/api/


Работа с пользвателем
---

### Регистрация:
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
### Авторизация
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

Работа с задачами
---

### Создание задачи
* Url: /tasks/
* Method: POST
* В Headers необходима авторизация через Authorization
* Request body (finish_date может не быть):
```json
{
  "title": "title",
  "description": "description",
  "status": "status",
  "finish_date": "finish_date"
}
```
* Response status 201 and body:
```json
{
  "id": "id_of_task",
  "title": "title",
  "description": "description",
  "status": "status",
  "finish_date": "finish_date"
}
```
***
### Получение списка всех задач
* Url: /tasks/
* Method: GET
* В Headers необходима авторизация через Authorization
* Возвращает только задачи авторизованного пользователя
* Response status 200 and body:
```json
[
  {
      "id": "id_of_task1",
      "title": "title1",
      "description": "description1",
      "status": "status1",
      "finish_date": "finish_date1"
  },
  {
      "id": "id_of_task2",
      "title": "title2",
      "description": "description2",
      "status": "status2",
      "finish_date": "finish_date2"
  }
]
```
***
### Получение конкретной задачи пользователя по id
* Url: /tasks/<int:id>/
* Method: GET
* В Headers необходима авторизация через Authorization
* Возвращает только задачи авторизованного пользователя, 
если задача с таким id не принадлежит авторизованному пользователю => вернется 404
* Response status 200 and body:
```json
{
      "id": "id",
      "title": "title",
      "description": "description",
      "status": "status",
      "finish_date": "finish_date"
  }
```
* Response status 404 and body:
```json
{
      "message": "User don't have task with that id"
}
```
***
### Изменение конкретной задачи пользователя по id
* Url: /tasks/<int:id>/
* Method: POST/PUT
* В Headers необходима авторизация через Authorization
* Работает только с задачами авторизованного пользователя, 
если задача с таким id не принадлежит авторизованному пользователю => вернется 404
* Request body (можно отправлять как одно из полей, так и несколько):
```json
{
  "title": "new_title"
}
```
```json
{
  "title": "new_title",
  "status": "new_status"
}
```
```json
{
  "title": "new_title",
  "description": "new_description",
  "status": "new_status",
  "finish_date": "new_finish_date"
}
```
* Response status 200 and body:
```json
{
      "id": "id",
      "title": "title",
      "description": "description",
      "status": "status",
      "finish_date": "finish_date"
  }
```
* Response status 400 and body (в случае указания статуса, не входящих в стандарные значения):
```json
{
      "message": "Status is not correct!"
}
```
* Response status 404 and body:
```json
{
      "message": "User don't have task with that id"
}
```
***

Работа с задачами
---
### Получение списка всех задач со статусом "Новая"
* Url: /new_tasks/
* Method: GET
* В Headers необходима авторизация через Authorization
* Возвращает только задачи авторизованного пользователя
* Response status 200 and body:
```json
[
  {
      "id": "id_of_task",
      "title": "title",
      "description": "description",
      "status": "New",
      "finish_date": "finish_date"
  }
]
```
***
### Получение списка всех задач со статусом "Запланированная"
* Url: /planned_tasks/
* Method: GET
* В Headers необходима авторизация через Authorization
* Возвращает только задачи авторизованного пользователя
* Response status 200 and body:
```json
[
  {
      "id": "id_of_task",
      "title": "title",
      "description": "description",
      "status": "Planned",
      "finish_date": "finish_date"
  }
]
```
***
### Получение списка всех задач со статусом "в Работе"
* Url: /planned_tasks/
* Method: GET
* В Headers необходима авторизация через Authorization
* Возвращает только задачи авторизованного пользователя
* Response status 200 and body:
```json
[
  {
      "id": "id_of_task",
      "title": "title",
      "description": "description",
      "status": "in Work",
      "finish_date": "finish_date"
  }
]
```
***
### Получение списка всех задач со статусом "Завершённая"
* Url: /planned_tasks/
* Method: GET
* В Headers необходима авторизация через Authorization
* Возвращает только задачи авторизованного пользователя
* Response status 200 and body:
```json
[
  {
      "id": "id_of_task",
      "title": "title",
      "description": "description",
      "status": "Compleated",
      "finish_date": "finish_date"
  }
]
```
***
### Получение списка всех задач отсортированных по возрастанию даты завершения
* Url: /sort_by_date_tasks/
* Method: GET
* В Headers необходима авторизация через Authorization
* Возвращает только задачи авторизованного пользователя
* Response status 200 and body:
```json
[
  {
      "id": "id_of_task",
      "title": "title",
      "description": "description",
      "status": "status",
      "finish_date": "finish_date"
  }
]
```
***