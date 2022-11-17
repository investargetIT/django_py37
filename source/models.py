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