#!/bin/bash

echo "📦 Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "📂 Applying migrations..."
python manage.py makemigrations
python manage.py migrate

echo "🧹 Collecting static files..."
python manage.py collectstatic --noinput

echo "🔑 Creating superuser..."
echo "Run 'python manage.py createsuperuser' manually if needed."

echo "🚀 Starting server..."
python manage.py runserver 127.0.0.1:8000