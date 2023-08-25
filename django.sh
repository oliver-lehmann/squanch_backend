#!/bin/bash

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    --run)
    RUN=true
    shift
    ;;
    --export)
    EXPORT=true
    shift
    ;;
    *)
    shift
    ;;
esac
done

if [ "$RUN" = true ]; then
    echo "Create migrations"
    python manage.py makemigrations sync
    echo "=============================="

    echo "Migrate"
    python manage.py migrate
    echo "=============================="

    echo "Start server"    
    python manage.py runserver

fi

if [ "$EXPORT" = true ]; then
    echo "Exporting packages to requirements.txt"
    conda list --export > requirements.txt
fi
