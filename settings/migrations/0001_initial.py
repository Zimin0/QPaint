# Generated by Django 4.2.3 on 2023-09-11 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebSiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Настройка')),
                ('value', models.CharField(max_length=255, verbose_name='Значение')),
            ],
        ),
    ]
