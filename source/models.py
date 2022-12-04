from django.db import models


class DataSource(models.Model):
    name = models.CharField(max_length=32, blank=True, unique=True)
    domain = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        super(DataSource, self).save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=32, blank=True, unique=True)
    datasource = models.ForeignKey(DataSource, on_delete=models.CASCADE, blank=True)

    def save(self, *args, **kwargs):
        super(Tag, self).save(*args, **kwargs)


class AuditStatus(models.Model):
    name = models.CharField(max_length=24, blank=True, unique=True)

    def save(self, *args, **kwargs):
        super(AuditStatus, self).save(*args, **kwargs)


class BDStatus(models.Model):
    name = models.CharField(max_length=24, blank=True, unique=True)

    def save(self, *args, **kwargs):
        super(BDStatus, self).save(*args, **kwargs)

class FamiliarLevel(models.Model):
    name = models.CharField(max_length=24, blank=True, unique=True)
    score = models.IntegerField(blank=True)

    def save(self, *args, **kwargs):
        super(FamiliarLevel, self).save(*args, **kwargs)

class Industry(models.Model):
    pid = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=24, blank=True)
    bucket = models.CharField(max_length=12, blank=True, null=True)
    key = models.CharField(max_length=128, blank=True, null=True)
    datasource = models.ForeignKey(DataSource, blank=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('pid', 'name', 'datasource')

    def save(self, *args, **kwargs):
        super(Industry, self).save(*args, **kwargs)

class IndGroup(models.Model):
    name = models.CharField(max_length=24, blank=True, unique=True)
    shareInvestor = models.BooleanField(default=False)
    manager = models.BigIntegerField(blank=True)
    ongoingurl = models.CharField(max_length=128, blank=True)
    datasource = models.ForeignKey(DataSource, blank=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'datasource')
    def save(self, *args, **kwargs):
        super(IndGroup, self).save(*args, **kwargs)

class OrgBDresponse(models.Model):
    name = models.CharField(max_length=32, blank=True, unique=True)
    material = models.CharField(max_length=32, blank=True)
    sort = models.IntegerField()

    def save(self, *args, **kwargs):
        super(OrgBDresponse, self).save(*args, **kwargs)

class OrgType(models.Model):
    name = models.CharField(max_length=32, blank=True, unique=True)

    def save(self, *args, **kwargs):
        super(OrgType, self).save(*args, **kwargs)

class Title(models.Model):
    name = models.CharField(max_length=32, blank=True, unique=True)
    score = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Title, self).save(*args, **kwargs)

class Country(models.Model):
    pid = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, blank=True, unique=True)
    bucket = models.CharField(max_length=12, blank=True, null=True)
    key = models.CharField(max_length=128, blank=True, null=True)
    level = models.PositiveSmallIntegerField(blank=True, default=1, verbose_name='洲、国、省、市、区')
    hot = models.IntegerField(blank=True, default=1, verbose_name='地区热度')

    def save(self, *args, **kwargs):
        super(Country, self).save(*args, **kwargs)

class MobileAddress(models.Model):
    '''
    手机号码归属地
    '''
    code = models.CharField(max_length=8, blank=True, unique=True)
    name = models.CharField(max_length=8, blank=True, verbose_name='地区名称')

    def save(self, *args, **kwargs):
        super(MobileAddress, self).save(*args, **kwargs)


class ClientType(models.Model):
    '''
    用户登录端类型
    '''
    name = models.CharField(max_length=20, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

class WebMenu(models.Model):
    '''
    网页菜单
    '''
    name = models.CharField(max_length=32, blank=True, null=True, unique=True)
    namekey = models.CharField(max_length=32, blank=True, null=True)
    icon_active = models.CharField(max_length=64, blank=True, null=True)
    icon_normal = models.CharField(max_length=64, blank=True, null=True, )
    parentmenu = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    index = models.SmallIntegerField(blank=True, default=1)

    def save(self, *args, **kwargs):
        super(WebMenu, self).save(*args, **kwargs)

