from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger # 导入 Paginator 类
from Sign.models import Event,Guest
#登录主页
def index(request):
    return render(request,"index.html")
#登录逻辑处理
def login_action(request):
    if request.method=='POST':
        login_username = request.POST.get("username")
        login_password = request.POST.get("password")
        if login_username == '' or login_password == '':
            return render(request, "index.html", {"error": "username or password not null"})
        else:
            user=auth.authenticate(username=login_username,password=login_password)
            if user is not None:
                auth.login(request,user)#验证登录
                response=HttpResponseRedirect("/event_manage/")
                #response.set_cookie('user',login_username,3600)
                request.session['user']=login_username
                return response
            else:
                return render(request, "index.html", {"error": "username or password error"})
    else:
        return render(request, "index.html")
#发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')  # 获取浏览器的session
    #发布会搜索
    search_name =request.GET.get('name','')
    events_=Event.objects.filter(name__contains=search_name)
    if len(events_) ==0:
        return render(request, "event_manage.html", {'user': username, 'hint': '查询结果为空，请重新输入！'})
    p = Paginator(events_, 3)
    page = request.GET.get('page')
    try:
        contacts = p.page(page)
    except PageNotAnInteger:
        contacts = p.page(1)
    except EmptyPage:
        contacts = p.page(p.num_pages)
    return render(request, "event_manage.html", {'user':username,'events': contacts,'name':search_name})
#发布会管理
@login_required
def event_manage(request):
    #username=request.COOKIES.get('user','')
    username=request.session.get('user','') #获取浏览器的session
    events_=Event.objects.all()
    if len(events_) ==0:
        return render(request, "event_manage.html", {'user': username, 'hint': '查询结果为空，请重新输入！'})
    p = Paginator(events_, 3)
    page = request.GET.get('page')
    try:
        contacts = p.page(page)
    except PageNotAnInteger:
        contacts = p.page(1)
    except EmptyPage:
        contacts = p.page(p.num_pages)
    return render(request, "event_manage.html", {'user':username,'events': contacts})
#嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')  # 获取浏览器的session
    #数据获取及分页处理
    guests_ = Guest.objects.all()
    if len(guests_) ==0:
        return render(request, "guest_manage.html", {'user': username, 'hint': '查询结果为空，请重新输入！'})
    p = Paginator(guests_, 3)
    page = request.GET.get('page')
    try:
        contacts = p.page(page)
    except PageNotAnInteger:
        contacts = p.page(1)
    except EmptyPage:
        contacts = p.page(p.num_pages)
    return render(request, "guest_manage.html", {'user': username, 'guests': contacts})
#嘉宾手机号搜索
@login_required
def search_phone(request):
    username = request.session.get('user', '')  # 获取浏览器的session
    #发布会搜索
    search_phone =request.GET.get('phone','')
    guests_ = Guest.objects.filter(phone__contains=search_phone)
    if len(guests_) ==0:
        return render(request, "guest_manage.html", {'user': username, 'hint': '查询结果为空，请重新输入！'})
    p = Paginator(guests_, 3)
    page = request.GET.get('page')
    try:
        contacts = p.page(page)
    except PageNotAnInteger:
        contacts = p.page(1)
    except EmptyPage:
        contacts = p.page(p.num_pages)
    return render(request, "guest_manage.html", {'user': username, 'guests': contacts,'phone':search_phone})
#嘉宾签到页面
@login_required
def sign_index(request,event_id):
    username = request.session.get('user', '')  # 获取浏览器的session
    event_id=get_object_or_404(Event,id=event_id)
    guest_list=Guest.objects.filter(event_id=event_id)
    sign_list = Guest.objects.filter(sign='1',event_id=event_id)
    guest_date=len(guest_list)
    sign_data = len(sign_list)
    return render(request, "sign_index.html", {'user': username,'event':event_id,'guest_date':guest_date,'sign_data':sign_data})
#嘉宾签到
@login_required
def sign_index_action(request,event_id):
    username = request.session.get('user', '')  # 获取浏览器的session
    event_id = get_object_or_404(Event, id=event_id)
    guest_list = Guest.objects.filter(event_id=event_id)
    sign_list = Guest.objects.filter(sign='1', event_id=event_id)
    guest_date = len(guest_list)
    sign_data = len(sign_list)
    phone=request.POST.get('phone','')
    if phone!="":
        result=Guest.objects.filter(phone=phone)
        if not result :
            return render(request, "sign_index.html",{'user': username, 'event': event_id,'hint':'phone error','guest_date':guest_date,'sign_data':sign_data})
        result=Guest.objects.filter(phone=phone,event_id=event_id)
        if not result :
            return render(request, "sign_index.html",{'user': username, 'event': event_id,'hint':'phone is not on the current release list','guest_date':guest_date,'sign_data':sign_data})
        result = Guest.objects.get(phone=phone, event_id=event_id)
        if result.sign:
            return render(request, "sign_index.html",{'user': username, 'event': event_id,'hint':'The user has checked in','guest_date':guest_date,'sign_data':sign_data})
        else:
            Guest.objects.filter(phone=phone, event_id=event_id).update(sign='1')
            return render(request, "sign_index.html",{'user': username,
                                                      'event': event_id,
                                                      'hint': 'Sign in successfully',
                                                      'guest_date': guest_date,
                                                      'sign_data': str(int(sign_data)+1),
                                                      'guest_sign':result})
    else:
        return render(request, "sign_index.html",{'user': username, 'event': event_id, 'guest_date': guest_date,'sign_data': sign_data})
#退出登录
@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/index/")
'''
get方法是从数据库的取得一个匹配的结果，返回一个对象，如果记录不存在的话，它会报错。
filter方法是从数据库的取得匹配的结果，返回一个对象列表，如果记录不存在的话，它会返回[]。
'''