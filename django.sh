#!/bin/bash
echo "Create migrations"
python manage.py makemigrations sync
echo "=============================="

echo "Migrate"
python manage.py migrate
echo "=============================="

echo "Start server"
python manage.py runserver