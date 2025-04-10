# OTUS_SERVER_LOGS
# Log Parser

Этот скрипт предназначен для анализа логов сервера в формате `access.log`. Он позволяет собирать статистику по HTTP-методам, IP-адресам, а также по самым длительным запросам.

## Описание

Скрипт выполняет следующие действия:
- Анализирует один или несколько лог-файлов.
- Собирает статистику по HTTP-методам (GET, POST, PUT, DELETE, OPTIONS, HEAD).
- Находит топ 3 IP-адреса с наибольшим количеством запросов.
- Выводит топ 3 самых длительных запросов.
- Сохраняет результаты анализа в JSON-формате.

## Установка и использование

1. Клонируйте репозиторий или скачайте скрипт.

2. Для анализа логов используйте команду:

   ```bash
   python log_parser.py <путь к файлу или директории с логами>