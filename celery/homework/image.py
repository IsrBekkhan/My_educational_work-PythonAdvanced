"""
Здесь происходит логика обработки изображения
"""

from typing import Optional

from PIL import Image, ImageFilter


def blur_image(src_filename: str, dst_filename: Optional[str] = None):
    """
    Функция принимает на вход имя входного и выходного файлов.
    Применяет размытие по Гауссу со значением 5.
    """
    if not dst_filename:
        dst_filename = f'blur_{src_filename}'

    with Image.open(src_filename) as img:
        img.load()
        new_img = img.filter(ImageFilter.GaussianBlur(5))
        new_img.save(dst_filename)
