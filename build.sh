#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --no-input

# Reset completo de la base de datos (borra todas las tablas)
python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('DROP SCHEMA public CASCADE;'); cursor.execute('CREATE SCHEMA public;'); print('Esquema reiniciado')"

# Aplicar todas las migraciones desde cero
python manage.py migrate

# Crear superusuario automáticamente si no existe
echo "from pasteleria_app.models import Usuarios; Usuarios.objects.create_superuser('admin', '4dm1n1234#') if not Usuarios.objects.filter(usuario='admin').exists() else None" | python manage.py shell