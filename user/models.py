import binascii
import datetime
import os

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models

from source.models import Tag, AuditStatus, IndGroup, DataSource, Title, MobileAddress, ClientType, FamiliarLevel
from util.baseclass import BaseModel, InvestError


class MyUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            source = request.META.get('HTTP_SOURCE')
            if not source:
                raise InvestError(code=800, msg='登录失败', detail='未知的datasoucre')
            if '@' not in username:
                user = User.objects.get(mobile=username, datasource_id=source)
            else:
                user = User.objects.get(email=username, datasource_id=source)
        except User.DoesNotExist:
            raise InvestError(code=404, msg='用户不存在')
        except Exception as err:
            raise InvestError(code=999, msg='MyUserBackend/authenticate模块验证失败\n, %s' % err)
        else:
            if user.check_password(password):
                return user
            else:
                raise InvestError(code=201)

    def user_can_authenticate(self, user):
        return True


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    name = models.CharField(max_length=32, blank=True, verbose_name='姓名')
    mobileAddress = models.ForeignKey(MobileAddress, blank=True, null=True, verbose_name='号码归属地', on_delete=models.SET_NULL)
    mobile = models.CharField(max_length=20, blank=True, verbose_name='手机号码')
    email = models.EmailField(max_length=64, blank=True, verbose_name='邮箱')
    auditStatus = models.ForeignKey(AuditStatus, blank=True, null=True, verbose_name='审核状态', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, blank=True, null=True, verbose_name='标签')
    indGroup = models.ManyToManyField(IndGroup, blank=True, null=True, verbose_name='行业组')
    title = models.ForeignKey(Title, blank=True, null=True, verbose_name='职位', on_delete=models.CASCADE)

    onJob = models.BooleanField(blank=True, default=True, help_text='是否在职')

    datasource = models.ForeignKey(DataSource, on_delete=models.CASCADE, blank=True)
    USERNAME_FIELD = 'mobile'
    objects = UserManager()


    class Meta:
        unique_together = (('mobile', 'datasource'), ('email', 'datasource'))
        permissions = (
        )

    def save(self, *args, **kwargs):
        return super(User, self).save(*args, **kwargs)

class UserToken(models.Model):
    key = models.CharField('Key', max_length=48, primary_key=True)
    user = models.ForeignKey(User, related_name='user_token',verbose_name=("MyUser"), on_delete=models.CASCADE)
    createtime = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    clientType = models.ForeignKey(ClientType, blank=True, help_text='登录类型', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_token'

    def timeout(self):
        return self.createtime < (datetime.datetime.now() - datetime.timedelta(hours=24 * 1))

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(UserToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(24)).decode()


class UserRelation(BaseModel):
    investor = models.ForeignKey(User, related_name='investor_relations', blank=True, verbose_name='投资人', on_delete=models.CASCADE)
    trader = models.ForeignKey(User, related_name='trader_relations', blank=True, verbose_name='交易师', on_delete=models.CASCADE)
    type = models.BooleanField(verbose_name='强弱关系类型', default=False, blank=True)
    familiar = models.ForeignKey(FamiliarLevel, null=True, blank=True, verbose_name='交易师熟悉度等级', on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        qs = UserRelation.objects.exclude(pk=self.pk).filter(investor=self.investor)
        if qs.exists():
            if qs.filter(trader=self.trader).exists():
                raise InvestError(code=405, msg='投资人交易师关系已存在')
            elif self.type and qs.filter(type=True).exists():
                self.relationtype = False
        if self.investor == self.trader:
            raise InvestError(code=2014, msg='投资人和交易师不能是同一个人')
        super(UserRelation, self).save(*args, **kwargs)