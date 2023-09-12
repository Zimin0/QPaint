from django.views.generic import TemplateView
from django.shortcuts import HttpResponse, redirect, render

class GetManualView(TemplateView):
    """ Главная страница - получить инструкцию, ..."""
    template_name = "manual/index.html"

class CodeView(TemplateView):
    """ Ввод кода из набора. """
    template_name = "manual/code.html"

    def post(self, request, *args, **kwargs):
        assembly_code = request.POST.get('coloring-code', None) # Код, который ввел юзер
        if True: # Если такой код не существует
            return render(request, self.template_name, {'message': "Такого кода не существует!"})
        return redirect('manual:version')
    
    def get(self, request, *args, **kwargs):
        return redirect(self.template_name)

class VersionView(TemplateView):
    """ Выбор типа набора - черно-белый, ... """
    template_name = "manual/type.html"

class UploadView(TemplateView):
    """ Загрузка картинки на обработку. """
    template_name = "manual/upload.html"
