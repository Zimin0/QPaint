from django.db import models

class WebSiteSettings(models.Model):
    """ Модель настроек приложения, редактируемых в админке """
    name = models.CharField(max_length=255, unique=True, verbose_name="Настройка")
    value = models.CharField(max_length=255, verbose_name="Значение")

# кол-во использований кода коструктора 
# почта для связи 