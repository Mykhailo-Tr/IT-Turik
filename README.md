# 🚀 IT-Turik — Шкільна система управління

![Project Banner](https://github.com/Mykhailo-Tr/IT-Turik/raw/main/banner.png)

---

## 📖 Проект

**IT-Turik** — це комплексний веб-додаток для автоматизації навчального процесу у школі. Система підтримує:
- Управління користувачами з ролями (учні, вчителі, адміністратори)
- Створення, редагування, видалення завдань та подій
- Керування предметами і дітьми
- Фільтрацію та пошук завдань за різними критеріями
- Адаптивний та зручний інтерфейс з динамічним оновленням через **AJAX**
- Інтерактивний календар для роботи з подіями через **FullCalendar**

Цей проєкт створений з урахуванням кращих практик веб-розробки, щоб допомогти школам підвищити ефективність управління навчанням.

---

## 🛠️ Технології та їх використання

| Технологія          | Опис                                        | Використання в проекті                                  |
|---------------------|---------------------------------------------|---------------------------------------------------------|
| ![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&style=flat-square) | Основна мова програмування | Серверна логіка, моделі, обробка запитів                |
| ![Django](https://img.shields.io/badge/Django-5.2-green?logo=django&style=flat-square) | Веб-фреймворк Python       | Вся архітектура проекту, маршрутизація, ORM, CBV        |
| ![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap&style=flat-square) | CSS фреймворк для UI       | Стилізація, адаптивний дизайн, модальні вікна, кнопки   |
| ![FullCalendar](https://img.shields.io/badge/FullCalendar-6.1.x-orange?logo=javascript&style=flat-square) | Бібліотека календарів      | Відображення і керування подіями у календарі            |
| ![SQLite](https://img.shields.io/badge/SQLite-3.39-lightgrey?logo=sqlite&style=flat-square) | База даних за замовчуванням| Зберігання даних користувачів, завдань, статусів        |
| ![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript&style=flat-square) | Скрипти для динаміки       | AJAX-запити, інтерактивність (прикріплення, видалення)  |
| ![Crispy Forms](https://img.shields.io/badge/django--crispy--forms-orange?logo=django&style=flat-square) | Гарне відображення форм    | Рендеринг форм з красивим HTML і Bootstrap класами      |
| ![Git](https://img.shields.io/badge/Git-F05032?logo=git&style=flat-square)           | Контроль версій            | Ведення історії розробки і командна робота              |

---


### Основні можливості:
- Інтеграція з [FullCalendar.io](https://fullcalendar.io/)
- Події створюються, редагуються і видаляються у модальних вікнах через AJAX
- Підтримка `all-day` подій, тривалих подій, перетягування
- Динамічне оновлення календаря після змін
- Валідація форм і оновлення через partial-шаблони


## 🏗 Архітектура

- Проект поділений на окремі додатки Django:
  - **accounts** — керування користувачами та ролями
  - **tasks** — робота із завданнями (CRUD, статуси, фільтри)
  - **events** — події (подібна логіка до завдань)
  - **calendarapp** — інтеграція з FullCalendar (створення/редагування подій через AJAX)
  - **dashboard** — основна панель користувача, керування акаунтами
- Використання **Class-Based Views (CBV)** для організації коду
- **RESTful** підхід у маршрутах
- **Рольова модель** з перевіркою доступу
- **AJAX** для динамічного оновлення даних без перезавантаження сторінок

---

## 🧩 Використані патерни програмування

- **Decorator (login_required)** — захист приватних сторінок
- **Mixin (Custom Permission Mixin)** — для повторного використання логіки доступу
- **Factory Pattern (get_or_create)** — створення або отримання статусів завдань
- **Template Inheritance** — єдина базова структура UI для всіх сторінок
- **Command Pattern** — окремі методи для дій, як-от toggle статусів
- **DRY (Don't Repeat Yourself)** — уникнення дублювання коду через CBV та міксини

---

## 🛠️ Інструкція для запуску

### Крок 1: Клонування репозиторію
```bash
git clone https://github.com/Mykhailo-Tr/IT-Turik.git
cd IT-Turik
```

### Крок 2: Віртуальне середовище (рекомендується)
```bash
python3 -m venv .venv

# Linux/macOS
source .venv/bin/activate
# Windows
.\.venv\Scripts\activate
```

### Крок 4: Встановлення залежностей
```bash
pip3 install -r requirements.txt

```


### Крок 5: Міграцій
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### Крок 6: Створення суперкористувача
```bash
python3 manage.py createsuperuser
```



### Крок 7: Запуск сервера
```bash
python3 manage.py runserver 127.0.0.0:8000
```



