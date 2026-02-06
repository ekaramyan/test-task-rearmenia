# API Test
## Разработано на:

* Python 3.10
* Веб-фреймворк FastAPI
* ORM SQLAlchemy + Alembic
* База данных Postgres

## Установка и запуск на локальной машине

1. Установить `Python 3.10`;
2. Установить `Virtual Env` с помощью командной строки;
```cmd
pip install virtualenv
```
3. Клонировать данный репозиторий с ветки `master`;
4. Перейти в консоли корень проекта
```cmd
cd ПУТЬ_К_ПРОЕКТУ
```
5. Создаём виртуальное окружение с помощью команды:
```cmd
virtualenv env
```
6. Активируем виртуальное окружение с помощью команды:
```c#
// Версия для Linux или MacOS//

source ./env/bin/activate
```
```c#
// Версия для Windows
// Если возникнет ошибка, то нужно предоставить права доступа на запуск .bat скриптов
./env/Scripts/activate
```
7. Убедиться что в консоли показывается что вы вошли в вирутальное окружение. Должно показывать слева строки название вашего окружения:
```
(env): _
```
8. Устанавливаем зависимости для нашего приложения:
```
pip install -r requirements.txt
```
9. Создаём `.env` файл в корне проекта и указываем в ней переменные нашего окружения:

```python
DB_NAME = НАЗВАНИЕ_БАЗЫ_ДАННЫХ
DB_LOGIN = ЛОГИН_ОТ_БАЗЫ_ДАННЫХ
DB_PASSWORD = ПАРОЛЬ_ОТ_БАЗЫ_ДАННЫХ
DB_HOST = ХОСТ_ГДЕ_НАХОДИТСЯ_БАЗА_ДАННЫХ
DB_PORT = ПОРТ_БАЗЫ_ДАННЫХ
JWT_SECRET_KEY = JWT_КЛЮЧ_ДЛЯ_ТОКЕНА
JWT_ALGORITHM = JWT_АЛГОРИТМ_ДЛЯ_КЛЮЧА
ACCESS_TOKEN_EXPIRE_MIRUTES = ВРЕМЯ_ЖИЗНИ_ACCESS_ТОКЕНА
REFRESH_TOKEN_EXPIRE_MIRUTES = ВРЕМЯ_ЖИЗНИ_REFRESH_ТОКЕНА
```

Пример заполненного `.env` файла:

```env
DB_LOGIN=postgres
DB_NAME=test_db
DB_PASSWORD=
DB_PORT=5432
DB_HOST=
AES_KEY=
JWT_SECRET_KEY=
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=24000
REFRESH_TOKEN_EXPIRE_MINUTES=100800

broker_host=localhost:9000
CURRENT_HOST=http://localhost:8000
OPENAI_API_KEY=
```
10. Запустим миграцию alembic:
```cmd
alembic upgrade head
```
11. Запускаем API на локальной машине с помощью команды:
```cmd
python3 main.py
```
12. После чего должно отобразиться следующий текст в консоли, который означает, что наш API запущен и можно с ним работать:
```
INFO:     Started server process [3340]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
* Чтобы выключить API нажмите сочетание клавиш Ctrl+C, чтобы выйти.
* Для выхода из вирутального окружения консоли, введите команду 
```
deactivate
```
13. Для перехода на Swagger документацию API, введите в адресной строке браузера http://127.0.0.1:8000/api/docs . После чего можете изучать и пробовать в самой документации все доступные роуты.

## Структура проекта
> `alembic` - папка миграции для базы данных

> `models` - папка для хранения бизнес-логики приложения

> `controllers` - папка с роутерами API;

> `views` - папка для хранения JSON / Database отображения данных

> `tests` - папка с unit тестами API;

> `database.py` - скрипт общего назначения для работы с базой данных;

> `main.py` - основной скрипт API;

> `requirements.txt` - текстовый файл для хранения списка зависимостей проекта;


## Написание Unit-тестов для API

### Полезные статьи для изучения
* Тестирование в FastAPI - https://fastapi.tiangolo.com/tutorial/testing/
* Тестирование БД в FastAPI - https://fastapi.tiangolo.com/advanced/testing-database/

Вы можете с лёгкостью писать необходимые unit-тесты для данного приложения. 

В папке `tests` создайте новый Python-скрипт к примеру `some_tests.py` . <br>

В созданном скрипте скопируйте и вставьте следующий стартовый шаблон:

```python
from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database import get_db, Base

# Импортируем тестируемые роутеры к примеру:

from routes.menu import router

#Импортируем тут необходимые нам БД модели к примеру:

from models.database.menu_models import Menu, MenuLink, MenuSection

#Импортируем тут необходимые нам JSON модели к примеру:

from models.database.json_models import Menu, MenuLink, MenuSection


# Укажем путь для нашей тестовой базы данных.
# Данный файл будет генерироваться автоматически!!
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app = FastAPI()

# Подключаем тестируемый роутер
app.include_router(router)

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_module(module):

    Base.metadata.create_all(bind=engine)
    db: Session = next(override_get_db())

    # Тут можно заранее указать те данные в БД которые нужно загрузить для тестирования
    db.add(Menu(id=1, name='test menu', parentid=None, type="", value=""))

    db.commit()


def teardown_module(module):
    # После окончания всех тестов, база данных будет полностью очищена (включая таблицы)
    Base.metadata.drop_all(engine)



# Тут уже пишутся ваши тесты
# .......



# Пример простого теста

def test__get_menus():

    # Получаем сессию БД
    db: Session = next(override_get_db())
    # Получаем строку из таблицы модели Menu с id=1  
    expected_res = db.query(Menu).get(1)

    #Делаем тестовый запрос к нашему API
    response = client.get("/menu/")
    
    #Проверка на успешный статус код
    assert response.status_code == 200
    # Проверяем, что JSON ответ совпадает с JSON представлением ожидаемого объекта Menu
    assert response.json() == [expected_res.to_json().dict()]
```

### Запуск тестов

Для запуска тестов укажите в консоле команду:
```
python -m pytest ./tests/ 
```
Или же команду дляз запуска определённого скрипта тестов:

```
python -m pytest ./tests/НАЗВАНИЕ_СКРИПТА.py 
```