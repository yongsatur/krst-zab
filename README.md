# Система управления проектами для Министерства сельского хозяйства Забайкальского края

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x-092E20?logo=django)](https://www.djangoproject.com/)

Это веб-приложение, разработанное по заказу для **Министерства сельского хозяйства Забайкальского края**. 
Платформа предназначена для управления проектами и данными в сфере агропромышленного комплекса региона.

## Цели и задачи

$`\color{yellow}*`$ Управление паспортами проектов;<br>
$`\color{yellow}*`$ Экспорт паспортов проектов в XLSX;<br>
$`\color{yellow}*`$ Учет пользователей по районам края.

## Стек технологий

$`\color{yellow}*`$ `Python` · `Django`<br>
$`\color{yellow}*`$ `HTML5` · `CSS3` · `JavaScript`<br>
$`\color{yellow}*`$ `Bootstrap 5`<br>
$`\color{yellow}*`$ `MySQL`

## Структура проекта

```
krst-zab/
├── krst/               # Основной конфигурационный модуль (настройки Django)
│   ├── ...       
├── passports/          # Приложение для работы с паспортами и документацией
│   ├── ...       
├── users/              # Приложение для управления пользователями и ролями
│   ├── ...       
├── templates           # HTML-шаблоны для всех страниц
├── static/             # Статические файлы
│   ├── css/
│   ├── js/
│   └── images/
├── manage.py           # Скрипт управления Django-проектом
├── requirements.txt 
└── README.md           
```
---

## Лицензия

Распространяется под лицензией [![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-red.svg)](LICENSE).
