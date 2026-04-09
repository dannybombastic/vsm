#!/bin/sh
set -e

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "⏳ Applying migrations..."
python manage.py migrate --noinput

echo "🌐 Compiling translations..."
python manage.py compilemessages --ignore=.venv 2>/dev/null || true

echo "📋 Loading questions..."
python manage.py load_questions

echo "✅ Ready!"
