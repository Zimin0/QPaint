# Generated by Django 4.2.3 on 2023-09-17 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manual', '0002_alter_constructor_manual_file_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assemblycode',
            options={'verbose_name': 'Код сборки из набора', 'verbose_name_plural': 'Коды сборки из наборов'},
        ),
        migrations.AlterModelOptions(
            name='constructor',
            options={'verbose_name': 'Конструктор картинки', 'verbose_name_plural': 'Конструкторы картинко'},
        ),
    ]
