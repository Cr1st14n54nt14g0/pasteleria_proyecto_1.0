#!/usr/bin/env bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate --noinput

# Crear superusuario automáticamente si no existe
echo "from pasteleria_app.models import Usuarios; Usuarios.objects.create_superuser('admin', '4dm1n1234#') if not Usuarios.objects.filter(usuario='admin').exists() else None" | python manage.py shell