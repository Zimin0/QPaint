from django.db import models
from datetime import datetime
import os

class AssemblyCode(models.Model):
    """ Код сборки, получаемый из физического набора """
    def __str__(self) -> str:
        return f"Код сборки №{self.pk}"
    
    class Meta:
        verbose_name = "Код сборки из набора"
        verbose_name_plural = "Коды сборки из наборов"

    code = models.CharField(max_length=20, verbose_name="Код набора", unique=True, blank=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    amount_of_usage = models.IntegerField(default=0)

class Constructor(models.Model):
    """ Создание конструктора пользователем - загрузка картинки и превращение ее в инструкцию по сборке """
    
    def __str__(self) -> str:
        return f"Конструктор картинки №{self.pk}"
    
    class Meta:
        verbose_name = "Конструктор картинки"
        verbose_name_plural = "Конструкторы картинко"

    def get_file_name(instance, filename):
        today = datetime.today()
        year = str(today.year)
        month = str(today.month).zfill(2)  # добавляем ведущий ноль, если месяц от 1 до 9
        day = str(today.day).zfill(2)      # добавляем ведущий ноль, если день от 1 до 9
        return os.path.join(year, month, day, filename)
    
    manual_file = models.FileField(verbose_name="Файл PDF инструкции", upload_to=get_file_name)
    slug = models.SlugField(verbose_name="Слаг")
    picture = models.ImageField(verbose_name="картинка JPG", upload_to=get_file_name)
    assemblycode = models.ForeignKey(AssemblyCode, verbose_name="Код-сборки", on_delete=models.SET_NULL, null=True)
    email = models.CharField(max_length=100, verbose_name="Почта", default="", null=True)

