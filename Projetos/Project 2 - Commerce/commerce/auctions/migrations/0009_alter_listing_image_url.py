# Generated by Django 3.2.3 on 2021-06-01 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_comment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image_url',
            field=models.URLField(blank=True, default='/auctions/static/images/no-proto.png', null=True),
        ),
    ]