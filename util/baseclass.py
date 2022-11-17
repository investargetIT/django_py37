from django.db import models
from source.models import DataSource

class BaseModel(models.Model):
    createtime = models.DateTimeField(auto_now_add=True, null=True)
    updatetime = models.DateTimeField(auto_now=True, null=True)
    datasource = models.ForeignKey(DataSource, on_delete=models.CASCADE, blank=True)

    def save(self, *args, **kwargs):
        super(BaseModel, self).save(*args, **kwargs)