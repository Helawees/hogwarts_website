# Hogwarts school website
Итоговый проект OTUS Python Developer. Basic course.

## Описание проекта
Данный проект представляет собой школьный веб-сайт по мотивам книг Гарри Поттер.
Вебсайт содержит информацию о факультетах, профессорах, учащихся, предметах и локациях.

## Функциональность
- Главная страница с базовой информацией о факультетах, кнопками для регистрации и авторизации
После регистрации и авторизации доступны следующие разделы:
- Houses (список факультетов и информация о них)
- Locations (список локаций школы)
- Professors (список преподавателей школы)
- Subjects (список предметов)
- Students (список студентов)
- Enroll in Hogwarts (зачисление нового студента на факультет, для группы пользователей Professors)
- Edit, Delete Student (из вкладки студенты, для группы пользователей Professors)
- Course enrollment (для группы пользователей Students)

## Технологии
Проект разработан с использованием следующих технологий:
- Python (Django)
- HTML, CSS, Bootstrap
- PostgreSQL 

## Зависимости
requirements.txt

Локальный хост http://127.0.0.1:8000/

## Структура проекта
```
hogwarts_website/
│── config/           # Стартовые настройки проекта 
│── hogwarts_app/     # Файлы приложения 
|   |----migrations   # Файлы миграций
|   |----static       # Статические файлы (CSS, JS, изображения, шрифты)
|   |----templates    # HTML-шаблоны
|   |----templatetags # кастомный фильтр групп пользователей
|   |----admin.py     # настройки административной части приложения
|   |----apps.py      # настройки приложения
|   |----forms.py     # формы
|   |----models.py    # модели
|   |----tests.py     # тесты
|   |----urls.py      # пути
|   |----views.py     # view-функции
│── manage.py         # Файл запуска
│── README.md         # Документация
│── requirements.txt  # Зависимости
```

## Автор
- Елена Чуева