from django.views.generic import TemplateView
from django.shortcuts import HttpResponse, redirect, render
from manual.models import AssemblyCode, Constructor 
from manual.business.PictureBusiness import CustomPictureBuilder
import json

class GetManualView(TemplateView):
    """ Главная страница - получить инструкцию, ..."""
    template_name = "manual/index.html"

class CodeView(TemplateView):
    """ Ввод кода из набора. """
    template_name = "manual/code.html"

    def post(self, request):
        assembly_code = request.POST.get('coloring-code', None) # Код, который ввел юзер
        db_code_query = AssemblyCode.objects.filter(code=assembly_code)
        if not db_code_query.exists(): # Если такой код не существует
            return render(request, self.template_name, {'message': "Такого кода не существует!"})
        db_code_obj = db_code_query.first() 
        if db_code_obj.amount_of_usage <= 0:
            return render(request, self.template_name, {'message': "У набора закончились конвертации!"})
        
        db_code_obj.amount_of_usage -= 1
        db_code_obj.save()
        request.session['assembly_code'] = assembly_code
        return redirect('manual:version')
    
    def get(self, request):
        return render(request, self.template_name)

class VersionView(TemplateView):
    """ Выбор типа набора - черно-белый, ... """
    template_name = "manual/type.html"
    def post(self, request):
        type_of_set = request.POST.get('coloring_type', None) 
        request.session['type_of_set'] = type_of_set
        return redirect('manual:upload')

class UploadView(TemplateView):
    """ Загрузка пользователем картинки на обработку. """
    template_name = "manual/upload.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        uploaded_file = request.FILES['cropped-photo']
        last_pic_paths = []
        path = Constructor.get_file_name(convert_id='11', tmp=True, only_path=True)
        for pic_color in range(7, 16, 2): 
            processor = CustomPictureBuilder(image_source=uploaded_file, BRIGHTNESS=pic_color/10, save_image_path=path)
            processor.process_image()
            last_pic_paths.append(processor.final_path)
        request.session['last_pic_paths'] = last_pic_paths
        new_constructor = Constructor.objects.create(
            json_pixels = processor.image_to_blocks(),
            assemblycode = AssemblyCode.objects.get(code=request.session.get("assembly_code", None)),
        )
        request.session['constructor_id'] = new_constructor.id
        return redirect('manual:choose_pic') 

class EmailView(TemplateView):
    """ Ввод почты для отправки инструкции. """
    template_name = "manual/email.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email_POST = request.POST.get('email', None)
        constr_id = request.session.get("constructor_id", False)
        if not constr_id:
            raise IndexError # поменять
        constructor = Constructor.objects.filter(id=constr_id)
        if constructor.exists():
            c1 = constructor.first()
            c1.email = email_POST
            c1.save()
        ##  Отправить письмо  ##
        import time
        time.sleep(2)
        return redirect('manual:get_instruction', constructor.first().slug )

class EmailSentView(TemplateView):
    """ Выводит страницу "Письмо отправлено!" или "Письмо не отправлено!" """
    ...

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
    
    def post(self, request):
        print(request.POST)
        request.session['choosen_picture'] = request.POST.get('coloring_photo')
        return redirect('manual:email')

class GetInstruction(TemplateView):
    """ Многостраничная инструкция по сборке."""
    template_name = 'manual/instruction.html'
    def get(self, request, instruction_slug):
        constr_objects = Constructor.objects.filter(slug=instruction_slug)
        if constr_objects.exists():
            constr_obj = constr_objects.first()
            return render(request, GetInstruction.template_name, {'instruction_slug':constr_obj.slug})

from django.http import JsonResponse
from django.views import View
from .models import Constructor
import json

class GetPixelsView(View):
    def get(self, request, instruction_slug, page_num):
        try:
            constr_obj = Constructor.objects.get(slug=instruction_slug)
            pixel_blocks = json.loads(constr_obj.json_pixels)
            pixel_blocks_one = pixel_blocks[page_num]
            return JsonResponse(pixel_blocks_one, safe=False)  # safe=False, так как pixel_blocks является списком, а не словарём
        except Constructor.DoesNotExist:
            return JsonResponse({"error": "Constructor not found"}, status=404)


"""  
request.session
choosen_picture - выбраная картинка (str:путь)
last_pic_paths - массив 6ти сгенерированных картинок (list)
constructor_id - id конструктора в бд
"""
