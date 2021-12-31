# Generated by Django 3.2.4 on 2021-08-05 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileserver',
            name='latitude',
            field=models.DecimalField(decimal_places=16, max_digits=22),
        ),
        migrations.AlterField(
            model_name='profileserver',
            name='longitude',
            field=models.DecimalField(decimal_places=16, max_digits=22),
        ),
    ]