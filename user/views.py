import datetime
import traceback

from django.contrib import auth
from rest_framework.decorators import api_view

from user.models import UserToken
from user.serializer import UserDetailSerializer
from util.baseclass import InvestError, JsonSuccessResponse, JsonInvestErrorResponse, JsonExceptionResponse
from util.basedef import CatchRequestException


# Create your views here.
@api_view(['POST'])
def login(request):
    try:
        data = request.data
        username = data.get('account')
        password = data.get('password')
        if not request.META.get('HTTP_CLIENTTYPE'):
            raise InvestError(code=2003, msg='登录失败，非法客户端', detail='登录类型不可用')
        user = auth.authenticate(request, username=username, password=password)
        if user.userstatus_id == 3:
            raise InvestError(2022, msg='登录失败，用户审核未通过，如有疑问请咨询工作人员。', detail='用户审核未通过')
        user.last_login = datetime.datetime.now()
        if not user.is_active:
            user.is_active = True
        user.save()
        perimissions = user.get_all_permissions()
        response = maketoken(user, request.META.get('HTTP_CLIENTTYPE'))
        response['permissions'] = perimissions
        response['is_superuser'] = user.is_superuser
        return JsonSuccessResponse(response)
    except InvestError as err:
        return JsonInvestErrorResponse(err)
    except Exception:
        CatchRequestException(request)
        return JsonExceptionResponse(traceback.format_exc().split('\n')[-2])


def maketoken(user,clienttype):
    tokens = UserToken.objects.filter(user=user, clienttype_id=clienttype)
    if tokens.exists():
        tokens.delete()
    token = UserToken.objects.create(user=user, clienttype_id=clienttype)
    serializer = UserDetailSerializer(user)
    return {'token': token.key,  "user_info": serializer.data}