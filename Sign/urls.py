from django.conf.urls import url
from Sign import views_api

urlpatterns = [
    url('add_event/', views_api.add_event,name='add_event'),
    #url('add_event/', views_api.add_event,name='add_event'),
]
