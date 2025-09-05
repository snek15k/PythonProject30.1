#!/bin/bash
set -e

APP_DIR="/home/${USER}/app"
VENV_DIR="$APP_DIR/venv"

echo ">>> Переходим в каталог приложения"
if [ ! -d "$APP_DIR" ]; then
  git clone https://github.com/<your-username>/<your-repo>.git $APP_DIR
fi

cd $APP_DIR
git fetch origin
git reset --hard origin/feature

echo ">>> Создаем виртуальное окружение (если нет)"
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv $VENV_DIR
fi

echo ">>> Активируем виртуальное окружение"
source $VENV_DIR/bin/activate

echo ">>> Обновляем pip и зависимости"
pip install --upgrade pip
pip install -r requirements.txt

echo ">>> Выполняем миграции и сбор статических файлов"
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo ">>> Перезапускаем gunicorn и nginx"
sudo systemctl restart gunicorn
sudo systemctl restart nginx

echo ">>> Деплой завершен успешно!"
