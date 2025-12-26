# Каталог оборудования (Django + DRF)

Каталог с иерархией площадок/цехов/типов, кастомными характеристиками, паспортами (файлы), корзиной, веб-UI и REST API.

## Возможности
- Иерархия: площадки → цеха, типы оборудования (дерево), оборудование с атрибутами (JSON).
- CRUD через веб-интерфейс и админку.
- Поиск/фильтры: имя/описание/инвентарный, тип, площадка/цех, пара `attribute_key/value`.
- Паспорта: загрузка файлов к оборудованию (через UI и API).
- Корзина для авторизованных.
- REST API (DRF) со списками/CRUD и пагинацией.
- Bootstrap UI (навигация, карточки, формы), загрузка изображений для оборудования.

## Быстрый старт
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # опционально, для /admin
python manage.py runserver
```
Открыть:  
- Веб: http://127.0.0.1:8000/  
- Админка: http://127.0.0.1:8000/admin/  
- API (browsable): http://127.0.0.1:8000/api/

## .env пример
Создайте `.env` в корне:
```
SECRET_KEY=замени-на-ключ
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
TIME_ZONE=Europe/Moscow
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
DEFAULT_FROM_EMAIL=noreply@example.com
```
Для проды: `DEBUG=False`, реальные `ALLOWED_HOSTS`, уникальный `SECRET_KEY`, secure-флаги по умолчанию True.

## API маршруты (основные)
- `GET/POST /api/equipment/` — список/создание оборудования, фильтры: `equipment_type`, `site`, `workshop`, `attribute_key`, `attribute_value`, `search`, `ordering`.
- `GET /api/equipment/{id}/` — детально.
- `GET /api/equipment/{id}/passports/` — паспорта конкретного оборудования.
- `GET/POST /api/equipment-types/`, `/api/sites/`, `/api/workshops/`.
- `GET/POST /api/passports/` — работа с паспортами (файлы).
- `GET/POST /api/cart/` — корзина текущего пользователя.

Аутентификация: Session/Basic (по умолчанию). Легко добавить JWT/Swagger при необходимости.

## Миграции и статика/медиа
- Миграции: `python manage.py migrate`
- Медиа (паспорта, изображения): `MEDIA_ROOT=media`, Django раздаёт в dev автоматически.

## Тесты и линт
```bash
python manage.py test
flake8
```

## Полезные ссылки
- Пользовательский UI: формы регистрации/логина, каталог, карточка товара с фото и паспортами, корзина.
- Админка: удобное управление типами, площадками, цехами, оборудованием, паспортами и корзиной.

## Что можно доработать при желании
- JWT и Swagger (drf-spectacular/drf-yasg).
- AJAX/SPA фронт, фильтры по вложенным атрибутам, предпросмотр изображений/кроп.
- Импорт/экспорт CSV/Excel, журналирование действий.

