from django.views.generic import TemplateView
from django.shortcuts import HttpResponse, redirect, render

from manual.models import AssemblyCode, Constructor # H24gGD85L

class GetManualView(TemplateView):
    """ Главная страница - получить инструкцию, ..."""
    template_name = "manual/index.html"

class CodeView(TemplateView):
    """ Ввод кода из набора. """
    template_name = "manual/code.html"

    def post(self, request, *args, **kwargs):
        assembly_code = request.POST.get('coloring-code', None) # Код, который ввел юзер
        if not AssemblyCode.objects.filter(code=assembly_code).exists(): # Если такой код не существует
            return render(request, self.template_name, {'message': "Такого кода не существует!"})
        request.session['assembly_code'] = assembly_code
        return redirect('manual:version')
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class VersionView(TemplateView):
    """ Выбор типа набора - черно-белый, ... """
    template_name = "manual/type.html"
    def post(self, request, *args, **kwargs):
        type_of_set = request.POST.get('coloring_type', None) 
        request.session['type_of_set'] = type_of_set
        print(type_of_set)
        return redirect('manual:upload')

class UploadView(TemplateView):
    """ Загрузка картинки на обработку. """
    template_name = "manual/upload.html"
