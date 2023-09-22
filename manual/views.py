from django.views.generic import TemplateView
from django.shortcuts import HttpResponse, redirect, render
from manual.models import AssemblyCode, Constructor # H24gGD85L
from manual.business.PictureBusiness import CustomPictureBuilder
from django.conf import settings
from django.http import JsonResponse
import os

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
        return redirect('manual:upload')

class UploadView(TemplateView):
    """ Загрузка пользователем картинки на обработку. """
    template_name = "manual/upload.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        uploaded_file = request.FILES['cropped-photo']
        # Указываем путь к директории для сохранения изображений
        # save_path = os.path.join(settings.MEDIA_ROOT,uploaded_file.name)

        # # Сохраняем изображение
        # with open(save_path, 'wb+') as destination:
        #     for chunk in uploaded_file.chunks():
        #         destination.write(chunk)
        last_pic_paths = []
        path = Constructor.get_file_name(convert_id='11', tmp=True, only_path=True)
        for pic_color in range(7, 18, 2): 
            processor = CustomPictureBuilder(image_source=uploaded_file, BRIGHTNESS=pic_color/10, save_image_path=path)
            pixels_data = processor.process_image()
            last_pic_paths.append(processor.final_path)
        request.session['last_pic_paths'] = last_pic_paths
        print(request.session['last_pic_paths'])
        # processor.image_to_blocks()
        # Нажата кнопка предпросмотра картинки
        # new_constructor = Constructor.objects.create(
        #     manual_file = ..., # получаем из бизнес логики
        #     picture = ..., # получаем из бизнес логики
        #     assemblycode = AssemblyCode.objects.get(code=request.session.get("assembly_code", None)),
        # )
        return redirect('manual:choose_pic') 

class EmailView(TemplateView):
    """ Ввод почты для отправки инструкции. """
    template_name = "manual/email.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', None)
        return redirect('manual:use_manual')

class UseManualView(TemplateView):
    """ Многостраничная инструкция по сборке """
    template_name = 'manual/instruction.html'

class ChoosePicView(TemplateView):
    """ Выбор из конвертированных картинок """
    template_name = 'manual/choose_photo.html'
    context = {}

    def get(self, request):
        paths_list_session = request.session.get("last_pic_paths", False)
        if not paths_list_session:
            print("Путей картинок нет в сессии !!!")
            ChoosePicView.context['pictures'] = []
        photos_list = []
        for path in paths_list_session:
            path = '/' + path
            path = path.replace('\\', '/')
            photos_list.append(path)
        ChoosePicView.context['pictures'] = photos_list
        return render(request, ChoosePicView.template_name, ChoosePicView.context)

class GetColorsJson(TemplateView):
    """ URL для запросов в фронта и получения массива цветов кратинки """
    ...

class GetPhotoesView(TemplateView):
    """ API для получения списка путей к 6ти картинкам """
    def get(self, request, *args, **kwargs):
        paths_list_session = request.session.get("last_pic_paths", False)
        if not paths_list_session:
            print("Путей картинок нет в сессии !!!")
            return JsonResponse([], safe=False)
        photos_list = []
        for path in paths_list_session:
            photos_list.append(path)
        return JsonResponse(photos_list, safe=False)