# ENNERO

Онлайн-магазин одежды на Django + SQLite.

Проект сделан как дипломная разработка: есть каталог, карточка товара, корзина, оформление заказа, админка и база данных.

---

## 1. Что это за проект

**ENNERO** — веб-приложение интернет-магазина одежды.

Что умеет:
- Главная страница с витриной
- Каталог с фильтрами
- Карточка товара (размер/цвет/остатки)
- Корзина
- Оформление заказа
- Сохранение заказов в БД
- Админ-панель для управления товарами и заказами

---

## 2. Технологии

- Python 3.12+ (у вас может быть 3.14)
- Django 6
- SQLite3 (файл `db.sqlite3`)
- Django Templates + CSS

---

## 3. Что нужно установить

Если вы запускаете первый раз на новом ПК:

1. Установить **Python** (с галочкой `Add Python to PATH`)
2. Установить **Git** (необязательно, но удобно)
3. Открыть **PowerShell** или терминал VS Code

Проверка, что Python установлен:

```powershell
python --version
```

Должно показать версию Python.

---

## 4. Быстрый запуск (самый короткий путь)

Откройте терминал в папке проекта `ClothesDiplomaPy` и выполните:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_shop --reset
python manage.py runserver 127.0.0.1:8090
```

После этого:
- Сайт: `http://127.0.0.1:8090/`
- Админка: `http://127.0.0.1:8090/admin/`

---

## 5. Очень подробный запуск (для новичков)

### Шаг 1. Перейти в папку проекта

```powershell
cd ClothesDiplomaPy
```

Если путь другой — используйте свой.

### Шаг 2. Создать виртуальное окружение

```powershell
python -m venv .venv
```

Это локальная «мини-среда» только для этого проекта.

### Шаг 3. Активировать окружение

```powershell
.\.venv\Scripts\activate
```

Если всё ок, в начале строки терминала появится `(.venv)`.

### Шаг 4. Установить зависимости

```powershell
pip install -r requirements.txt
```

### Шаг 5. Применить миграции (создать структуру БД)

```powershell
python manage.py migrate
```

### Шаг 6. Заполнить демо-данными (товары/категории)

```powershell
python manage.py seed_shop --reset
```

`--reset` удалит старые демо-данные каталога и создаст их заново.

### Шаг 7. Запустить сервер

```powershell
python manage.py runserver 127.0.0.1:8090
```

Откройте в браузере:
- `http://127.0.0.1:8090/`

Остановить сервер: `Ctrl + C`.

---

## 6. Как зайти в админку

### Создать администратора (один раз)

```powershell
python manage.py createsuperuser
```

Дальше введите:
- username
- email (можно пусто)
- пароль

### Вход

- Откройте `http://127.0.0.1:8090/admin/`
- Введите созданный логин/пароль

В админке можно управлять:
- категориями
- товарами
- изображениями
- вариантами товара (размер/цвет/остаток)
- заказами

---

## 7. Как пользоваться как обычный пользователь

1. Открыть сайт `/`
2. Перейти в каталог
3. Открыть товар
4. Выбрать вариант (размер/цвет)
5. Добавить в корзину
6. Перейти в корзину
7. Нажать «Оформить заказ»
8. Заполнить форму
9. Получить страницу успешного заказа

---

## 8. Важные команды (на каждый день)

```powershell
# Запуск сервера
python manage.py runserver 127.0.0.1:8090

# Проверка Django-конфига
python manage.py check

# Создать/обновить миграции после изменений моделей
python manage.py makemigrations
python manage.py migrate

# Сбросить и заново заполнить каталог демо-данными
python manage.py seed_shop --reset

# Запустить тесты
python manage.py test shop
```

---

## 9. Структура проекта

```text
ClothesDiplomaPy/
├─ config/                       # Настройки Django проекта
│  ├─ settings.py
│  ├─ urls.py
│  └─ ...
├─ shop/                         # Основное приложение магазина
│  ├─ models.py                  # Таблицы БД
│  ├─ views.py                   # Логика страниц
│  ├─ urls.py                    # Маршруты
│  ├─ cart.py                    # Корзина (session-based)
│  ├─ forms.py                   # Формы checkout/contacts
│  ├─ admin.py                   # Настройка админки
│  ├─ templates/shop/            # HTML шаблоны
│  └─ management/commands/
│     └─ seed_shop.py            # Команда заполнения БД
├─ static/shop/styles.css        # Стили
├─ db.sqlite3                    # Файл БД SQLite
├─ requirements.txt              # Зависимости Python
└─ manage.py                     # CLI Django
```

---

## 10. Типичные проблемы и решения

### Проблема: `python` не найден

Решение:
- переустановите Python
- включите `Add Python to PATH`
- перезапустите терминал

### Проблема: нельзя активировать `.venv` (ExecutionPolicy)

Решение в PowerShell (один раз):

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Потом снова:

```powershell
.\.venv\Scripts\activate
```

### Проблема: порт занят (`Address already in use`)

Решение:
- запустите на другом порту:

```powershell
python manage.py runserver 127.0.0.1:8091
```

### Проблема: нет таблиц / ошибки БД

Решение:

```powershell
python manage.py migrate
```

### Проблема: пустой каталог

Решение:

```powershell
python manage.py seed_shop --reset
```

---

## 11. Данные и БД

Используется SQLite (`db.sqlite3`).

Ключевые сущности:
- `Category`
- `Product`
- `ProductImage`
- `ProductVariant`
- `Order`
- `OrderItem`

Связи:
- `Category 1 -> N Product`
- `Product 1 -> N ProductVariant`
- `Product 1 -> N ProductImage`
- `Order 1 -> N OrderItem`

---

## 12. Статус проекта

Проект работает локально как полноценный онлайн-магазин одежды ENNERO.

Если нужно, следующим шагом можно добавить:
- оплату через реальный платежный провайдер
- личный кабинет пользователя
- избранное
- автотесты для критичных сценариев

---

## 13. Короткая памятка

Каждый раз при работе:

```powershell
cd ClothesDiplomaPy
.\.venv\Scripts\activate
python manage.py runserver 127.0.0.1:8090
```

Готово.
