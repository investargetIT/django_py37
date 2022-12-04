from django.db import models
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

from source.models import DataSource
from util.responsecode import responsecode


class BaseModel(models.Model):
    createtime = models.DateTimeField(auto_now_add=True, null=True)
    lastmodifytime = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(BaseModel, self).save(*args, **kwargs)

class InvestError(Exception):
    def __init__(self, code, msg=None, detail=None):
        self.code = code
        self.msg = msg if msg else responsecode[str(code)]
        self.detail_msg = detail if detail else responsecode[str(code)]

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data=data)
        kwargs['content_type'] = 'application/json; charset=utf-8'
        super(JSONResponse, self).__init__(content , **kwargs)

class JsonSuccessResponse(HttpResponse):
    def __init__(self, result, **kwargs):
        data = {'code': 1000, 'errormsg': None, 'result': result, 'detail': None}
        content = JSONRenderer().render(data=data)
        kwargs['content_type'] = 'application/json; charset=utf-8'
        super(JsonSuccessResponse, self).__init__(content , **kwargs)

class JsonInvestErrorResponse(HttpResponse):
    def __init__(self, investError, **kwargs):
        data = {'code': investError.code, 'errormsg': investError.msg, 'result': None, 'detail': investError.detail_msg}
        content = JSONRenderer().render(data=data)
        kwargs['content_type'] = 'application/json; charset=utf-8'
        super(JsonInvestErrorResponse, self).__init__(content , **kwargs)

class JsonExceptionResponse(HttpResponse):
    def __init__(self, msg, **kwargs):
        data = {'code': 9999, 'errormsg': '系统错误，请联系工作人员', 'result': None, 'detail': msg}
        content = JSONRenderer().render(data=data)
        kwargs['content_type'] = 'application/json; charset=utf-8'
        super(JsonExceptionResponse, self).__init__(content , **kwargs)


