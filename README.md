# LEVELUP

Интернет-магазин видеоигр на Django + SQLite.

Дипломный проект: каталог игр, карточка с выбором платформы и издания, корзина, оформление заказа, заявки с контактов, админ-панель.

---

## 1. Что это за проект

**LEVELUP** — веб-приложение интернет-магазина видеоигр.

Что умеет:
- Главная страница с витриной и жанровыми подборками
- Каталог с фильтрами (платформа, рейтинг PEGI, категория, цена, наличие)
- Карточка игры (платформа / издание / остатки)
- Корзина
- Оформление заказа (наличными или картой)
- Сохранение заказов в БД
- Форма контактов — заявки сохраняются в базе
- Админ-панель: игры, заказы, заявки с контактов

---

## 2. Технологии

- Python 3.12+
- Django 6
- SQLite3 (файл `db.sqlite3`)
- Django Templates + CSS (gaming-дизайн, без Bootstrap)

---

## 3. Что нужно установить

1. Установить **Python** (с галочкой `Add Python to PATH`)
2. Открыть **PowerShell** или терминал

Проверка:

```powershell
python --version
```

---

## 4. Быстрый запуск

Открой терминал в папке проекта и выполни:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_shop --reset
python manage.py runserver 127.0.0.1:8000
```

После этого:
- Сайт: `http://127.0.0.1:8000/`
- Админка: `http://127.0.0.1:8000/admin/`

---

## 5. Подробный запуск (для новичков)

### Шаг 1. Создать виртуальное окружение

```powershell
python -m venv .venv
```

### Шаг 2. Активировать окружение

```powershell
# Windows
.\.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate
```

Должно появиться `(.venv)` в начале строки терминала.

### Шаг 3. Установить зависимости

```powershell
pip install -r requirements.txt
```

### Шаг 4. Создать структуру БД

```powershell
python manage.py migrate
```

### Шаг 5. Заполнить демо-данными (игры + категории)

```powershell
python manage.py seed_shop --reset
```

`--reset` удалит старые демо-данные и создаст 8 категорий и 8 игр заново.

### Шаг 6. Запустить сервер

```powershell
python manage.py runserver
```

Открой: `http://127.0.0.1:8000/`  
Остановить: `Ctrl + C`

---

## 6. Как зайти в админку

### Создать администратора (один раз)

```powershell
python manage.py createsuperuser
```

Ввести: username, email (можно пусто), пароль.

### Вход

`http://127.0.0.1:8000/admin/`

В админке можно управлять:
- Категориями игр
- Играми (с изображениями и вариантами платформ/изданий)
- Заказами (смена статуса: Новый → В обработке → Завершён)
- **Заявками с контактов** (обращения клиентов, смена статуса: Новая / В работе / Обработана)

---

## 7. Как пользоваться как покупатель

1. Открыть сайт `/`
2. Перейти в каталог
3. Открыть игру
4. Выбрать вариант (платформа / издание)
5. Добавить в корзину
6. Перейти в корзину
7. Нажать «Оформить заказ»
8. Заполнить форму и выбрать оплату
9. Получить страницу подтверждения заказа

---

## 8. Важные команды

```powershell
# Запуск сервера
python manage.py runserver

# Создать/применить миграции после изменений моделей
python manage.py makemigrations
python manage.py migrate

# Сбросить и заново заполнить каталог демо-данными
python manage.py seed_shop --reset

# Проверка конфига Django
python manage.py check
```

---

## 9. Структура проекта

```
LEVELUP/
├── config/                    # Настройки Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
├── shop/                      # Основное приложение магазина
│   ├── models.py              # Таблицы БД
│   ├── views.py               # Логика страниц
│   ├── urls.py                # Маршруты
│   ├── cart.py                # Корзина (session-based)
│   ├── forms.py               # Формы оформления и контактов
│   ├── admin.py               # Настройка админки
│   ├── templates/shop/        # HTML-шаблоны
│   └── management/commands/
│       └── seed_shop.py       # Команда заполнения БД
├── static/shop/styles.css     # Стили (gaming dark-тема)
├── requirements.txt           # Зависимости Python
├── manage.py                  # CLI Django
└── info.md                    # Полная документация проекта
```

---

## 10. База данных

Используется SQLite (`db.sqlite3`).

Ключевые модели:
- `Category` — категории игр (Action, RPG, PS5, PC Games…)
- `Product` — игры (название, разработчик, рейтинг PEGI, цена, скидка)
- `ProductImage` — обложки игр
- `ProductVariant` — варианты (платформа + издание + остаток на складе)
- `Order` — заказы покупателей
- `OrderItem` — позиции заказа
- `ContactRequest` — заявки с формы контактов

Связи:
```
Category     1 → N  Product
Product      1 → N  ProductVariant
Product      1 → N  ProductImage
Order        1 → N  OrderItem
```

---

## 11. Типичные проблемы

### `python` не найден
Переустановить Python с галочкой `Add Python to PATH`, перезапустить терминал.

### Нельзя активировать `.venv` (ExecutionPolicy)
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Порт занят
```powershell
python manage.py runserver 127.0.0.1:8001
```

### Пустой каталог / ошибки БД
```powershell
python manage.py migrate
python manage.py seed_shop --reset
```

---

## 12. Статус проекта

Проект работает локально как полноценный интернет-магазин видеоигр LEVELUP.

При необходимости можно добавить:
- Оплату через реальный платёжный провайдер
- Личный кабинет покупателя
- Избранные игры
- Автотесты для критичных сценариев

---

## 13. Короткая памятка

```powershell
.\.venv\Scripts\activate
python manage.py runserver
```

Готово.

---

> Полная документация (архитектура, таблицы БД, разбор кода, вопросы комиссии) — в файле **`info.md`**
