import datetime
import traceback

from django_py37.settings import APILOG_PATH


#记录request error
def CatchRequestException(request):
    now = datetime.datetime.now()
    filepath = APILOG_PATH['excptionlogpath'] + '/' + now.strftime('%Y-%m-%d')
    f = open(filepath, 'a')
    f.writelines(now.strftime('%H:%M:%S') +
                 '发起用户id:' + str(request.user.id) +
                 'path:' + request.path +
                 'method:' + request.method + '\n' +
                 traceback.format_exc() + '\n\n')
    f.close()