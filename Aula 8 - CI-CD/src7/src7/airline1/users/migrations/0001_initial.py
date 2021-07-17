# Generated by Django 3.2.3 on 2021-06-04 20:50
import os
from django.db import migrations

# Criei uma migration empy usando 
# python manage.py makemigrations --empty users
# Para cirar django superuser logo ao iniciar o container
class Migration(migrations.Migration):

    initial = True

    def create_superuser(apps, schema_editor):
        from django.contrib.auth.models import User

        DJANGO_DB_NAME = os.environ.get('DJANGO_DB_NAME', "default")
        DJANGO_SU_NAME = os.environ.get('DJANGO_SU_NAME', "admin")
        DJANGO_SU_EMAIL = os.environ.get('DJANGO_SU_EMAIL', "admin@example.com")
        DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SU_PASSWORD', "1234")

        if (DJANGO_DB_NAME != "" and DJANGO_SU_NAME != "" and
            DJANGO_SU_EMAIL != "" and DJANGO_SU_PASSWORD != ""):
            superuser = User.objects.create_superuser(
                username=DJANGO_SU_NAME,
                email=DJANGO_SU_EMAIL,
                password=DJANGO_SU_PASSWORD)

        superuser.save()

    # initial = true, então não tem dependencias;
    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]

    