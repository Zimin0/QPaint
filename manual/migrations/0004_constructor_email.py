# Generated by Django 4.2.3 on 2023-09-17 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manual', '0003_alter_assemblycode_options_alter_constructor_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='constructor',
            name='email',
            field=models.CharField(default='', max_length=100, null=True, verbose_name='Почта'),
        ),
    ]
