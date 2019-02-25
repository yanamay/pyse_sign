from django.http import JsonResponse
from Sign.models import Event, Guest
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError
import time
#添加发布会
def add_event(request):
    if request.method == 'POST':
        eid = request.POST.get('eid', '')  # 发布会id
        name = request.POST.get('name', '')  # 发布会标题
        limit = request.POST.get('limit', '')  # 限制参与人数
        address = request.POST.get('address', '')  # 发布会地址
        status = request.POST.get('status', '')  # 发布状态
        start_time = request.POST.get('start_time', '')  # 发布会开始时间
        create_time = request.POST.get('create_time', '')  # 发布会创建时间

        if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
            return JsonResponse({'status': 10021, 'message': '参数不能为空'})
        try:
            int(eid)
        except ValueError:
            return JsonResponse({'status': 10022, 'message': 'eid格式错误'})
        try:
            int(limit)
        except ValueError:
            return JsonResponse({'status': 10023, 'message': 'limit格式错误'})
        try:
            int(limit)
        except ValueError:
            return JsonResponse({'status': 10024, 'message': 'limit格式错误'})
        result=Event.objects.filter(id=eid)
        if result:
            return JsonResponse({'status': 10025, 'message': 'eid已存在'})
        result = Event.objects.filter(name=name)
        if result:
            return JsonResponse({'status': 10026, 'message': 'name已存在'})
        if status == '':
            status = False
        if create_time=='':
            create_time=start_time
        try:
            Event.objects.create(id=eid,name=name,limit=limit,address=address,status=status,create_time=create_time,start_time=start_time)
        except ValidationError:
            error = '开始时间格式错误. 必须是YYYY-MM-DD HH:MM:SS格式'
            return JsonResponse({'status': 10027, 'message': error})
    else:
        return JsonResponse({'status': 10031, 'message': '请求方式错误'})

