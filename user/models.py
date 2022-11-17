from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from source.models import Tag
from util.baseclass import BaseModel


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    name = models.CharField(32, blank=True, verbose_name='姓名')
    mobile = models.CharField(max_length=11, blank=True, verbose_name='手机号码')
    email = models.EmailField(max_length=64, blank=True, verbose_name='邮箱')
    tag = models.ManyToManyField(Tag, blank=True)

    class Meta:
        permissions = (
        )

    def save(self, *args, **kwargs):
        return super(User, self).save(*args, **kwargs)