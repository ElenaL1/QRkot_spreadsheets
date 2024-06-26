### Сервис для кошачего благотворительного фонда
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

Стек технологий
FastAPI, Alembic, SQLAlchemy, Google API

### Локальное развертывание проекта
Клонировать репозиторий, cоздать виртуальное окружение, обновить установщик пакетов pip, установить зависимости:
```
py 3.9 -m venv venv
source venv/Scripts/activate
pip install --upgrade pip
pip install -r requirements.txt
```
Создать файл .env в корне проекта с данными в след. формате:
```
APP_TITLE=Благотворительный фонд поддержки котиков QRKot
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secret
FIRST_SUPERUSER_EMAIL=admin@admin.ru
FIRST_SUPERUSER_PASSWORD=admin
```
Применить миграции:
```
alembic upgrade head
```
Запустить проект:
```
uvicorn app.main:app --reload
```

Документация: localhost:8000/docs

Пример endpoints в API:

Регистрация пользователя
`POST /auth/register/`
```
{
  "email": "user@example.com",
  "password": "string"
}
```
Более подробную информацию см. в файле openapi.json.
Для просмотра документации загрузите файл на сайт https://redocly.github.io/redoc/. Вверху страницы есть кнопка Upload a file, нажмите её и загрузите скачанный файл. Спецификация проекта отобразится в формате ReDoc.