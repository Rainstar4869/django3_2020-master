import os
import uuid

from django.db import models
from imagekit.processors import ResizeToFill
from imagekit.models import ImageSpecField
import logging

logger = logging.getLogger("error_logger")


def product_avatar_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("product", filename)
    # return "avatar/product_{0}/{1}".format(instance.id, filename)


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True, default=None)
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    image = models.ImageField(null=True, upload_to=product_avatar_path)
    thumb_image = ImageSpecField(  # 注意：ImageSpecField 不会生成数据库表的字段
        source='image',
        processors=[ResizeToFill(256, 256)],  # 处理成一寸照片的大小
        format='JPEG',  # 处理后的图片格式
        options={'quality': 95}  # 处理后的图片质量
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "store"

    def __str__(self):
        return self.name

    def avatar_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return '/mediafiles/default/product_default.jpg'

    def thumb_avatar_url(self):
        if self.thumb_image and hasattr(self.thumb_image, 'url'):
            return self.thumb_image.url
        else:
            return '/media/default/thumb_product_default.jpg'
