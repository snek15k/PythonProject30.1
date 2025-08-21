# Проект Django + Celery + Redis + PostgreSQL

## Запуск через Docker Compose

1. Клонировать репозиторий:
   ```bash
   git clone <repo_url>
   cd <repo_name>
2. Создайте файл .env в корне проекта на основе .env.example и заполните нужные переменные:

cp .env.example .env


3. Соберите контейнеры и запустите проект:

docker-compose up --build


4. После запуска проект будет доступен по адресу:
👉 http://localhost:8000