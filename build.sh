#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
#python manage.py makemigrations pasteleria_app --noinput
#python manage.py migrate --noinput


python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); cursor.execute(\"DELETE FROM django_migrations WHERE app='pasteleria_app'\"); print('Migraciones eliminadas')"
python manage.py migrate pasteleria_app
python manage.py migrate


# Crear superusuario automáticamente si no existe
echo "from pasteleria_app.models import Usuarios; Usuarios.objects.create_superuser('admin', '4dm1n1234#') if not Usuarios.objects.filter(usuario='admin').exists() else None" | python manage.py shell