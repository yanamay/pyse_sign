from django.db import models

class Event(models.Model):
    name=models.CharField(max_length=100) #发布会标题
    limit=models.IntegerField() #限制参与人数
    status=models.BooleanField() #发布会状态
    address=models.CharField(max_length=200) #发布会地址
    start_time=models.DateTimeField() #发布会时间
    create_time=models.DateTimeField(auto_now=True) #发布会创建时间
    class Meta:
        ordering=['-id'] #分页数据不满一页时，去掉警告信息
    def __str__(self):
        return self.name

class Guest(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE) #关联发布会id
    realname=models.CharField(max_length=20) #姓名
    phone=models.CharField(max_length=11) #手机号
    email=models.EmailField() #邮箱
    sign=models.BooleanField() #签到状态
    create_time=models.DateTimeField(auto_now=True) #创建时间
    class Meta:
        unique_together=('phone','event')
        ordering=['-id']
    def __str__(self):
        return  self.realname
