from django.db import models
from datetime import datetime
import os
import random
import string

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
    
    def generate_slug():
        """ Генерирует слаг для конструктора """
        alphabet = string.ascii_letters
        slug = ''
        for _ in range(10):
            slug += random.choice(alphabet) 
        return slug

    def get_file_name(instance=None, filename:str=None, convert_id:str=None, tmp:bool=False, only_path:bool=False):
        """ tmp - временная директория """
        today = datetime.today()
        year = str(today.year)
        month = str(today.month).zfill(2)  # добавляем ведущий ноль, если месяц от 1 до 9
        day = str(today.day).zfill(2)      # добавляем ведущий ноль, если день от 1 до 9
        file_path = os.path.join('media', year, month, day)
        if convert_id is not None:
            file_path = os.path.join(file_path, convert_id)
        if tmp:
            file_path = os.path.join(file_path, 'tmp')
        # Проверяем существование директории и создаем, если она не существует
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        else:  # Если директория существует и не пуста, удаляем все файлы из неё
            for file in os.listdir(file_path):
                os.remove(os.path.join(file_path, file))
        if only_path:
            return file_path
        return os.path.join(file_path, filename)
    
    class Meta:
        verbose_name = "Конструктор картинки"
        verbose_name_plural = "Конструкторы картинкок"
    
    manual_file = models.FileField(verbose_name="Файл PDF инструкции", upload_to=get_file_name, null=True)
    slug = models.SlugField(verbose_name="Слаг", null=True, default=generate_slug)
    picture = models.ImageField(verbose_name="картинка JPG", upload_to=get_file_name, null=True)
    assemblycode = models.ForeignKey(AssemblyCode, verbose_name="Код-сборки", on_delete=models.SET_NULL, null=True)
    json_pixels = models.TextField(null=True, blank=True) # editable = False
    email = models.CharField(max_length=100, verbose_name="Почта", default="", null=True)

