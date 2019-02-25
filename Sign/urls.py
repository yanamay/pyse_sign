from django.conf.urls import url
from Sign import views_api

urlpatterns = [
    url('add_event/', views_api.add_event,name='add_event'),
    url('get_event_list/', views_api.get_event_list,name='get_event_list'),
    url('add_guest/', views_api.add_guest,name='add_guest'),
    url('get_guest_list/', views_api.get_guest_list,name='get_guest_list'),
    url('user_sign/', views_api.user_sign,name='user_sign'),
]
