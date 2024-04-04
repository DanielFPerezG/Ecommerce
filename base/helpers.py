import io
from PIL import Image
from resizeimage import resizeimage
import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

class ImageHandler:
    @staticmethod
    def save_resized_image_create(temp_file, img, object, type):
        with open(temp_file.name, 'rb') as f:
            with Image.open(f) as image:
                if type == "productHome":
                    cover = resizeimage.resize_cover(image, [370, 390])
                    output = io.BytesIO()
                    cover.save(output, format='JPEG', quality=100)
                    output.seek(0)
                    object.image.save(img.name, ContentFile(output.read()), save=False)
                elif type == "productDetail":
                    cover = resizeimage.resize_cover(image, [770, 400])
                    output = io.BytesIO()
                    cover.save(output, format='JPEG', quality=100)
                    output.seek(0)
                    object.imageDetail.save(img.name, ContentFile(output.read()), save=False)
                elif type == "productDetailSecond":
                    cover = resizeimage.resize_cover(image, [770, 400])
                    output = io.BytesIO()
                    cover.save(output, format='JPEG', quality=100)
                    output.seek(0)
                    object.imageDetailSecond.save(img.name, ContentFile(output.read()), save=False)
                elif type == "banner":
                    cover = resizeimage.resize_cover(image, [790, 680])
                    output = io.BytesIO()
                    cover.save(output, format='JPEG', quality=100)
                    output.seek(0)

                    object.image.save(img.name, ContentFile(output.read()), save=False)

                elif type == "Topic":
                    cover = resizeimage.resize_cover(image, [385, 330])
                    output = io.BytesIO()
                    cover.save(output, format='JPEG', quality=100)
                    output.seek(0)
                    object.image.save(img.name, ContentFile(output.read()), save=False)

    @staticmethod
    def save_resized_image_update(image, type):
        with Image.open(image) as img:
            if type == "productHome":
                cover = resizeimage.resize_cover(img, [370, 390])
            elif type == "productDetail":
                cover = resizeimage.resize_cover(img, [770, 400])
            elif type == "productDetailSecond":
                cover = resizeimage.resize_cover(img, [770, 400])
            elif type == "banner":
                cover = resizeimage.resize_cover(img, [790, 680])
            elif type == "Topic":
                cover = resizeimage.resize_cover(img, [385, 330])
            output = io.BytesIO()
            cover.save(output, format='JPEG', quality=100)
            output.seek(0)
            return ContentFile(output.read())