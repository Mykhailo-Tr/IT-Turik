# 🚀 SchoolSys — School Management System

![Project Banner](https://github.com/Mykhailo-Tr/IT-Turik/raw/main/banner.png)

---

## 📖 Project Overview

**SchoolSys** is a comprehensive web application designed to automate the educational process in schools. The system supports:
- Role-based user management (students, teachers, administrators)
- Creation, editing, and deletion of tasks and events
- Subject and child management
- Filtering and searching tasks based on various criteria
- Responsive and user-friendly interface with **AJAX** updates
- Interactive calendar functionality via **FullCalendar**

This project follows best web development practices to enhance the efficiency of managing educational workflows.

---

## 🛠️ Technologies Used

| Technology          | Description                                | Usage in Project                                         |
|---------------------|--------------------------------------------|----------------------------------------------------------|
| ![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&style=flat-square) | Main programming language | Server-side logic, models, request handling               |
| ![Django](https://img.shields.io/badge/Django-5.2-green?logo=django&style=flat-square) | Python web framework       | Project architecture, routing, ORM, CBV                   |
| ![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap&style=flat-square) | CSS framework              | Styling, responsive UI, modals, buttons                   |
| ![FullCalendar](https://img.shields.io/badge/FullCalendar-6.1.x-orange?logo=javascript&style=flat-square) | Calendar library           | Event rendering and manipulation in the calendar          |
| ![SQLite](https://img.shields.io/badge/SQLite-3.39-lightgrey?logo=sqlite&style=flat-square) | Default database            | Stores user data, tasks, statuses                         |
| ![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript&style=flat-square) | Dynamic interaction         | AJAX requests, interactivity                              |
| ![Crispy Forms](https://img.shields.io/badge/django--crispy--forms-orange?logo=django&style=flat-square) | Form rendering tool         | Beautiful form rendering with Bootstrap                   |
| ![Git](https://img.shields.io/badge/Git-F05032?logo=git&style=flat-square)           | Version control system      | Code history and team collaboration                      |

---

### Key Features
- Integration with [FullCalendar.io](https://fullcalendar.io/)
- Events created, edited, and deleted through AJAX-powered modals
- Supports all-day and multi-day events with drag-and-drop
- Calendar refreshes dynamically upon event changes
- Form validation and partial template updates

## 🏗 Architecture

- Modular Django structure with separate apps:
  - **accounts** — user and role management
  - **tasks** — task CRUD operations, filters, statuses
  - **events** — event handling
  - **calendarapp** — AJAX-based FullCalendar integration
  - **dashboard** — user panel and account control
- Use of **Class-Based Views (CBV)** for clean logic
- **RESTful** URL design
- Role-based access control
- **AJAX** used for dynamic, non-refresh page updates

---

## 🧩 Design Patterns Implemented

- **Decorator (login_required)** — restrict access to private views
- **Mixin (Custom Permission Mixin)** — reusable access logic
- **Factory Pattern (get_or_create)** — create or retrieve task statuses
- **Template Inheritance** — unified UI layout via base templates
- **Command Pattern** — encapsulated logic (e.g., toggle status)
- **DRY Principle** — eliminate code repetition via CBV and helpers

---

## 🛠️ Project Setup Instructions

### Step 1: Clone the repository
```bash
git clone https://github.com/Mykhailo-Tr/IT-Turik.git
cd IT-Turik
```

### Step 2: Create a virtual environment (recommended)
```bash
python3 -m venv .venv

# Linux/macOS
source .venv/bin/activate
# Windows
.\.venv\Scripts\activate
```

### Step 3: Install dependencies
```bash
pip3 install -r requirements.txt
```

### Step 4: Run migrations
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### Step 5: Create a superuser
```bash
python3 manage.py createsuperuser
```

### Step 6: Run the development server
```bash
python3 manage.py runserver 127.0.0.1:8000
```
