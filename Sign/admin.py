from django.contrib import admin
from Sign.models import Event,Guest

#发布会页面处理
class EventAdmin(admin.ModelAdmin):
    list_display = ['name','limit','status','address','start_time'] #页面显示字段
    search_fields = ['name'] #搜索栏
    list_filter = ['status'] #过滤器

#嘉宾页面处理
class GuestAdmin(admin.ModelAdmin):
    list_display = ['event','realname','phone','sign','email']
    search_fields = ['realname'] #搜索栏
    list_filter = ['sign'] #过滤器
admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)