from django.db import models


class DataSource(models.Model):
    name = models.CharField(max_length=32, blank=True)
    domain = models.CharField(max_length=64, blank=True)

    def save(self, *args, **kwargs):
        super(DataSource, self).save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=32, blank=True)
    datasource = models.ForeignKey(DataSource, on_delete=models.CASCADE, blank=True)

    def save(self, *args, **kwargs):
        super(Tag, self).save(*args, **kwargs)


class AuditStatus(models.Model):
    name = models.CharField(max_length=24, blank=True)

    def save(self, *args, **kwargs):
        super(AuditStatus, self).save(*args, **kwargs)


class BDStatus(models.Model):
    name = models.CharField(max_length=24, blank=True)

    def save(self, *args, **kwargs):
        super(BDStatus, self).save(*args, **kwargs)

class Familiarlevel(models.Model):
    name = models.CharField(max_length=24, blank=True)
    score = models.IntegerField(blank=True)

    def save(self, *args, **kwargs):
        super(Familiarlevel, self).save(*args, **kwargs)

class Industry(models.Model):
    PindustryID = models.IntegerField()
    name = models.CharField(max_length=24, blank=True)
    bucket = models.CharField(max_length=12, blank=True)
    key = models.CharField(max_length=128, blank=True)
    datasource = models.ForeignKey(DataSource, on_delete=models.CASCADE, blank=True)

    def save(self, *args, **kwargs):
        super(Industry, self).save(*args, **kwargs)

class Group(models.Model):
    name = models.CharField(max_length=24, blank=True)
    shareInvestor = models.BooleanField(default=False)
    manager = models.BigIntegerField(blank=True)
    ongongingurl = models.CharField(max_length=128, blank=True)
    datasource = models.ForeignKey(DataSource, on_delete=models.CASCADE, blank=True)

    def save(self, *args, **kwargs):
        super(Group, self).save(*args, **kwargs)
