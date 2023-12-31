""" 
sharpness contrast brightness
    0        1.6      1.3 (не очень темные)
    0         0       2.3 (очень темные и не контрасные)
"""
""" 
pictures
1. Bright one (Девушка у стены)
https://pp.userapi.com/t9RZfxBoVV30lGBnWqwdhneTBchjfwApL18-Dg/xwnsNhP5m1I.jpg
2. Dark one (Мужик смотрит вверх)
https://thumbs.dreamstime.com/z/%D1%82%D0%B5%D0%BC%D0%BD%D0%BE%D0%B5-%D0%B8%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BF%D0%BE%D1%80%D1%82%D1%80%D0%B5%D1%82%D0%B0-%D0%B7%D1%80%D0%B5%D0%BB%D0%BE%D0%B3%D0%BE-%D1%87%D0%B5%D0%BB%D0%BE%D0%B2%D0%B5%D0%BA%D0%B0-136721259.jpg
3. Dark one (Темнокожая девушка)
https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRsw-ZqhdgmXtOjB0djQS9FqAHl1bzbCdx4CbKSiqDDSQ0ZAqgnGRZsn3jmXAYmwyknEVw&usqp=CAU
"""


from django.http import JsonResponse
from PIL import Image, ImageEnhance, ImageFilter
from urllib.request import urlopen
import os
import random
import string
import json

class CustomPictureBuilder:
    """
    self.output_path - путь до картинки
    self.name - название файла картинки
    """
    WIDTH = 120 # ширина картинки
    HEIGHT = 160 # высота картинки
    BLOCK_WIDTH = 10 
    BLOCK_HEIGHT = 16
    BASE_COLORS = [
        (0, 0, 0),
        (64, 64, 64),
        (100, 100, 100),
        (130, 130, 130),
        (255, 255, 255)
    ]

    def __init__(self, image_source, BRIGHTNESS=1, SHARPNESS=3, CONTRAST=1.4, save_image_path=None):
        self.save_image_path = save_image_path
        self.BRIGHTNESS = BRIGHTNESS # 1.5
        self.SHARPNESS = SHARPNESS # 3
        self.CONTRAST = CONTRAST # 1.4
        if isinstance(image_source, str):
            self.image = self.open_image(image_source)
        else:
            # Если предоставлен объект файла
            self.image = Image.open(image_source)
    
    def open_image(self, path_or_url):
        """ 
        Открывает изображение по локальному пути или URL.
        Возвращает объект изображения PIL.
        """
        if path_or_url.startswith(('http://', 'https://')):
            with urlopen(path_or_url) as response:
                return Image.open(response)
        else:
            return Image.open(path_or_url)
    
    def _generate_random_file_name(self):
        """ Генерирует случайное имя для картинки """
        random_letters = ''.join(random.choice(string.ascii_letters) for _ in range(7))
        self.name = f"PIC_{random_letters}.jpg"
        return self.name
    
    def save_image(self): 
        if self.save_image_path is None: # если папка не задана программистом при инициализации объекта 
            path_to_media_folder=os.getcwd()
        else:
            path_to_media_folder = self.save_image_path
        self.output_path = os.path.join(path_to_media_folder, self._generate_random_file_name())
        self.image.save(self.output_path, "JPEG")
        return self.output_path
    
    def get_black_white_pic_average(self):
        """ Функция ниже находит ближайший к пикселю цвет из заданной черно-белой палитры и заполняет ими новую картинку """
        image_processed = Image.new('RGB', (self.image.size[0], self.image.size[1]))
        original_pixels = self.image.load() # получаем пиксели оригинального изображения 
        pixels_processed = image_processed.load() # получаем пустые пиксели нового изображения 
        choosen = self.BASE_COLORS[-1]

        for x in range(self.image.size[0]): # добавить предсказание пикселя по цвету прошлого
            for y in range(self.image.size[1]):
                delta = 256
                pixel_color = original_pixels[x, y]
                average = max(0, int(sum(pixel_color)/3))
                for b_color in self.BASE_COLORS:
                    new_delta = abs(b_color[0] - average)
                    if new_delta <= delta:
                        delta = new_delta
                        choosen = b_color
                    else:
                        break
                pixels_processed[x, y] = choosen
        self.image = image_processed
    
    def enhance(self, mode, factor):
        enhancer = {
            "sharpness": ImageEnhance.Sharpness,
            "contrast": ImageEnhance.Contrast,
            "brightness": ImageEnhance.Brightness
        }.get(mode)(self.image)
        self.image = enhancer.enhance(factor)

    def apply_smooth(self):
        """ Применяет сглаживание к картинке"""
        self.image = self.image.filter(ImageFilter.SMOOTH)

    def resize(self):
        """ Меняет размер картинки на кол-во кубиков в наборе """
        self.image = self.image.resize((CustomPictureBuilder.WIDTH, CustomPictureBuilder.HEIGHT), Image.Resampling.LANCZOS)
    
    def get_json_pixels(self):
        """ Создает json файл со всеми цветами пикселей изображения. Не используется. """
        pixels_list = self.image_to_blocks()
        with open("data.json", "w", encoding='utf-8') as file:
            json.dump(pixels_list, file)
        return pixels_list # должен возвращать путь до файла 
    
    def image_to_blocks(self):
        """
        Преобразует изображение в массив блоков пикселей.
        """
        pixels = list(self.image.getdata())
        blocks = []        
        for i in range(0, self.image.width, self.BLOCK_WIDTH):
            for j in range(0, self.image.height, self.BLOCK_HEIGHT): 
                block = []
                for x in range(self.BLOCK_WIDTH):
                    for y in range(self.BLOCK_HEIGHT):
                        if i + x < self.image.width and j + y < self.image.height:
                            block.append(list(pixels[(i + x) + (j + y) * self.image.width]))
                blocks.append(block)
        return blocks

    def blocks_to_image(self, blocks):
        """
        Восстанавливает изображение из блоков пикселей.
        """
        image = Image.new("RGB", (self.image.width, self.image.height))
        draw = image.load()
        block_index = 0
        for i in range(0, self.image.width, self.BLOCK_WIDTH):
            for j in range(0, self.image.height, self.BLOCK_HEIGHT):
                pixel_index = 0
                for x in range(self.BLOCK_WIDTH):
                    for y in range(self.BLOCK_HEIGHT):
                        if i + x < self.image.width and j + y < self.image.height:
                            draw[i + x, j + y] = tuple(blocks[block_index][pixel_index])
                            pixel_index += 1
                block_index += 1
        self.image = image

    def process_image(self):
        """ Применяет все нужные фильтры к картинке """
        self.enhance("brightness", self.BRIGHTNESS)
        self.enhance("sharpness", self.SHARPNESS)
        self.enhance("contrast", self.CONTRAST)
        self.image = self.image.convert('RGB') # конвертирует из rgba В rgb
        self.apply_smooth()
        self.resize()
        self.get_black_white_pic_average()
        pixels_data = self.get_json_pixels()
        self.final_path = self.save_image()
        return pixels_data

# processor = CustomPictureBuilder("D:\\JOB\\freelance11Qbrix\\paints\\media\\cropped_photo.jpg", BRIGHTNESS=1, SHARPNESS=3, CONTRAST=1.4)
# pixels_data = processor.process_image()