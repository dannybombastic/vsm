#!/bin/sh
set -e

echo "⏳ Applying migrations..."
python manage.py migrate --noinput

echo "🌐 Compiling translations..."
python manage.py compilemessages --ignore=.venv 2>/dev/null || true

echo "📋 Loading questions..."
python manage.py load_questions

echo "✅ Ready!"
