import uuid

from allauth.account.signals import user_logged_in
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db.models.signals import post_save
from django.dispatch import receiver
from imagekit.processors import ResizeToFill
from imagekit.models import ImageSpecField
# Create your models here.
from rest_framework_simplejwt.tokens import RefreshToken
import logging
from django.conf import settings

from mptt.models import MPTTModel, TreeForeignKey

logger = logging.getLogger("error_logger")


class UserManager(BaseUserManager):
    def create_user(self, username, email, parent_introcode=None, password=None):
        if username is None:
            raise TypeError("Users should have a username")
        if email is None:
            raise TypeError("Users should have a Email")
        if parent_introcode is None:
            raise TypeError("parent_introcode is needed")

        user = self.model(username=username,
                          email=self.normalize_email(email),
                          parent_introcode=parent_introcode,
                          is_active=False)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError("Password should not be None")

        user = self.create_user(username, email, None, password)
        User.objects.filter(email=email).update(is_superuser=True, is_staff=True)

        return user


def user_avatar_path(instance, filename):
    return "avatar/user_{0}/{1}".format(instance.id, filename)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True, default=None)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    introcode = models.UUIDField(default=uuid.uuid4())
    parent_introcode = models.UUIDField(blank=True, null=True, default=None)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, upload_to=user_avatar_path)
    thumb_avatar = ImageSpecField(  # 注意：ImageSpecField 不会生成数据库表的字段
        source='avatar',
        processors=[ResizeToFill(256, 256)],  # 处理成一寸照片的大小
        format='JPEG',  # 处理后的图片格式
        options={'quality': 95}  # 处理后的图片质量
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    class Meta:
        app_label = "authentication"

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return '/mediafiles/default/user.jpg'

    def thumb_avatar_url(self):
        if self.thumb_avatar and hasattr(self.thumb_avatar, 'url'):
            return self.thumb_avatar.url
        else:
            return '/media/default/thumb_user.jpg'


# @receiver(user_logged_in)  # Decorator of receiving signal while user going to logged in
# def post_login(sender, user, request, response, **kwargs):
#     logger.error("after user login")
#     response.set_cookie('team', 'india')  # This will set cookie
#     return response


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        logger.error("post_save create_user")
        try:
            if instance.parent_introcode:
                parent = User.objects.get(introcode=instance.parent_introcode)
            else:
                parent = User.objects.get(username=settings.ADMIN_NAME)
        except ObjectDoesNotExist:
            parent = User.objects.get(username=settings.ADMIN_NAME)

        logger.error(parent)

        try:
            parent_profile = Profile.objects.get(user__username=parent.username)
            user_profile = Profile.objects.create(user=instance, parent=parent_profile)
            logger.error("normal use profile created")
            logger.error(user_profile)
        except ObjectDoesNotExist:
            user_profile = Profile.objects.create(user=instance, parent=None)
            logger.error("ObjectDoesNotExist use profile created")
            logger.error(user_profile)


class Profile(MPTTModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    # class MPTTMeta:
    #     order_insertion_by = ['introcode']

    def __str__(self):
        return "{}'s profile".format(self.user.username)
