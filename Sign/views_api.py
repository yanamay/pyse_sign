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
        result=Event.objects.filter(id=eid)
        if result:
            return JsonResponse({'status': 10024, 'message': 'eid已存在'})
        result = Event.objects.filter(name=name)
        if result:
            return JsonResponse({'status': 10025, 'message': 'name已存在'})
        if status == '':
            status = False
        try:
            Event.objects.create(id=eid,name=name,limit=limit,address=address,status=status,start_time=start_time)
        except ValidationError:
            error = '开始时间格式错误. 必须是YYYY-MM-DD HH:MM:SS格式'
            return JsonResponse({'status': 10026, 'message': error})
    else:
        return JsonResponse({'status': 10031, 'message': '请求方式错误'})
#发布会查询
def get_event_list(request):
    if request.method=='GET':
        eid = request.GET.get('eid', '')  # 发布会id
        name = request.GET.get('name', '')  # 发布会名称

        if eid == '' and name== '' :
            return JsonResponse({'status':10021,'message':'参数不能为空'})
        if eid!='':
            event={}
            try:
                int(eid)
            except ValueError:
                return JsonResponse({'status': 10022, 'message': 'eid格式错误'})
            try:
                result=Event.objects.get(id=eid)
            except ObjectDoesNotExist:
                return JsonResponse({'status': 10023, 'message': '查询结果为空'})
            else:
                event['eid']=result.id
                event['name']=result.name
                event['limit'] = result.limit
                event['address'] = result.address
                event['status'] = result.status
                event['start_time'] = result.start_time
                return JsonResponse({'status':200,'message':'成功','data':event})
        if name!='':
            datas=[]
            results=Event.objects.filter(name__contains=name)
            if results:
                for r in results:
                    event = {}
                    event['eid'] = r.id
                    event['name'] = r.name
                    event['limit'] = r.limit
                    event['address'] = r.address
                    event['status'] = r.status
                    event['start_time'] = r.start_time
                    datas.append(event)
                return JsonResponse({'status': 200, 'message': '成功', 'data': datas})
            else:
                return JsonResponse({'status': 10024, 'message': '查询结果为空'})
    else:
        return JsonResponse({'status':10031,'message':'请求方式错误'})
#添加嘉宾
def add_guest(request):
    if request.method == 'POST':
        eid = request.POST.get('eid', '')  # 关联发布会id
        realname = request.POST.get('realname', '') #姓名
        phone = request.POST.get('phone', '')  # 手机号
        email = request.POST.get('email', '')  # 邮箱
        if eid == '' or realname == '' or phone == '':
            return JsonResponse({'status': 10021, 'message': '参数不能为空'})
        try:
            int(eid)
        except ValueError:
            return JsonResponse({'status': 10022, 'message': 'eid格式错误'})
        try:
            int(phone)
        except ValueError:
            return JsonResponse({'status': 10023, 'message': 'phone格式错误'})
        result = Event.objects.filter(id=eid)
        if not result:
            return JsonResponse({'status': 10024, 'message': 'Event id为空'})
        result = Event.objects.get(id=eid).status
        if not result:
            return JsonResponse({'status': 10025, 'message': '发布会未开启'})
        event_limit = Event.objects.get(id=eid).limit  # 发布会限制人数
        guest_limit = Guest.objects.filter(event_id=eid)  # 发布会已添加的嘉宾数
        if len(guest_limit) >= event_limit:
            return JsonResponse({'status': 10026, 'message': '发布会人数限制已满'})

        event_time = Event.objects.get(id=eid).start_time  # 发布会时间
        timeArray=time.strptime(str(event_time),'%Y-%m-%d %H:%M:%S')
        e_time=int(time.mktime(timeArray))
        now_time=str(time.time()) #获取当前时间
        ntime=now_time.split('.')[0]
        n_time=int(ntime)
        if n_time>=e_time:
            return JsonResponse({'status': 10027, 'message': '发布会已开始或已结束'})

        try:
            Guest.objects.create(realname=realname, phone=phone, email=email, sign=0, event_id=eid)
        except IntegrityError:
            return JsonResponse({'status': 10026, 'message': '活动嘉宾手机号码重复'})
    else:
        return JsonResponse({'status': 10031, 'message': '请求方式错误'})
# 嘉宾查询
def get_guest_list(request):
    if request.method == 'GET':
        eid = request.GET.get('eid', '')  # 发布会关联id
        phone=request.GET.get('phone', '')  # 嘉宾手机号
        if eid != '' and phone=='':
            try:
                int(eid)
            except ValueError:
                return JsonResponse({'status': 10021, 'message': 'eid格式错误'})
            datas = []
            results = Guest.objects.filter(event_id=eid)
            if results:
                for r in results:
                    guest = {}
                    guest['id'] = r.id
                    guest['realname'] = r.realname
                    guest['phone'] = r.phone
                    guest['email'] = r.email
                    guest['sign'] = r.sign
                    guest['create_time'] = r.create_time
                    guest['eid'] = r.event_id
                    datas.append(guest)
                return JsonResponse({'status': 200, 'message': '成功', 'data': datas})
            else:
                return JsonResponse({'status': 10022, 'message': '查询结果为空'})
        else:
            return JsonResponse({'status': 10028, 'message': 'eid不能为空'})
        if eid != '' and phone!='':
            try:
                int(eid)
            except ValueError:
                return JsonResponse({'status': 10024, 'message': 'eid格式错误'})
            try:
                int(phone)
            except ValueError:
                return JsonResponse({'status': 10025, 'message': 'phone格式错误'})
            guests = {}
            try:
                result = Guest.objects.get(phone=phone,event_id=eid)
                guests['id'] = result.id
                guests['realname'] = result.realname
                guests['phone'] = result.phone
                guests['email'] = result.email
                guests['sign'] = result.sign
                guests['create_time'] = result.create_time
                guests['eid'] = result.event_id
                return JsonResponse({'status': 200, 'message': '成功', 'data': guests})
            except ObjectDoesNotExist:
                return JsonResponse({'status': 10026, 'message': '查询结果为空'})
        else:
            return JsonResponse({'status': 10027, 'message': 'eid不能为空'})
    else:
        return JsonResponse({'status': 10031, 'message': '请求方式错误'})
# 嘉宾签到
def user_sign(request):
    if request.method == 'POST':
        eid = request.POST.get('eid', '')  # 关联发布会id
        phone = request.POST.get('phone', '')  # 手机号
        if eid == '' and phone == '':
            return JsonResponse({'status': 10021, 'message': '参数不能为空'})
        try:
            int(eid)
        except ValueError:
            return JsonResponse({'status': 10022, 'message': 'eid格式错误'})
        try:
            int(phone)
        except ValueError:
            return JsonResponse({'status': 10023, 'message': 'phone格式错误'})
        result = Event.objects.filter(id=eid)
        if not result:
            return JsonResponse({'status': 10024, 'message': 'Event id为空'})
        result = Event.objects.get(id=eid).status
        if not result:
            return JsonResponse({'status': 10025, 'message': '发布会未开启'})

        event_time = Event.objects.get(id=eid).start_time  # 发布会时间
        timeArray=time.strptime(str(event_time),'%Y-%m-%d %H:%M:%S')
        e_time=int(time.mktime(timeArray))
        now_time=str(time.time()) #获取当前时间
        ntime=now_time.split('.')[0]
        n_time=int(ntime)
        if n_time>=e_time:
            return JsonResponse({'status': 10025, 'message': '发布会已开始或已结束'})

        result = Guest.objects.filter(phone=phone)
        if not result:
            return JsonResponse({'status': 10026, 'message': '嘉宾手机号未填写'})
        result = Guest.objects.filter(event_id=eid, phone=phone)
        if not result:
            return JsonResponse({'status': 10027, 'message': '嘉宾未参加发布会'})
        result = Guest.objects.get(event_id=eid, phone=phone).sign
        if result:
            return JsonResponse({'status': 10028, 'message': '用户已签到'})
        else:
            Guest.objects.filter(event_id=eid, phone=phone).update(sign='1')
            return JsonResponse({'status': 200, 'message': '签到成功'})
    else:
        return JsonResponse({'status': 10031, 'message': '请求方式错误'})