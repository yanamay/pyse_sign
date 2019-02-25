from django.test import TestCase
from datetime import datetime
from django.contrib.auth.models import User
from Sign.models import Event, Guest
from django.test import Client

class IndexPageTest(TestCase):
    #测试index
    def test_index_page_renders_index_template(self):
        #断言是否用给定的index.html模板响应
        response=self.client.get('/index/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')
class LoginActionPageTest(TestCase):
    #测试登录动作
    def setUp(self):
        User.objects.create_user(username='admin',password='111111',email='admin@qq.com')
    def test_login_action_username_password_null(self):
        #用户名和密码为空
        user_info={'username':'','password':''}
        response=self.client.post('/login_action/',data=user_info)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'username or password not null',response.content)
    def test_login_action_username_password_error(self):
        #用户名和密码输入错误
        user_info={'username':'admin','password':'123456'}
        response=self.client.post('/login_action/',data=user_info)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'username or password error',response.content)
    def test_login_action_success(self):
        #登录成功
        user_info={'username':'admin','password':'111111'}
        response=self.client.post('/login_action/',data=user_info)
        self.assertEqual(response.status_code,302)
class EventMangeTest(TestCase):
    #发布会管理
    def setUp(self):
        User.objects.create_user(username='admin',password='111111',email='admin@qq.com')
        Event.objects.create(name ='xiaomi5',limit =20,status =False,
                             address ='chendu',
                             start_time =datetime(2019,2,22,14,0,0),
                             create_time =datetime(2019,2,22,13,0,0))
        login_user = {'username': 'admin', 'password': '111111'}
        self.client.post('/login_action/', data=login_user)  # 预先登录
    def test_event_mange_success(self):
        #测试发布会信息获取
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b"xiaomi5",response.content)
        self.assertIn(b"chendu", response.content)
    def test_event_mange_search_success(self):
        #测试发布会信息搜索
        response = self.client.get('/search_name/',{'name':'xiaomi5'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"xiaomi5",response.content)
        self.assertIn(b"chendu", response.content)
class GuestManageTest(TestCase):
    #嘉宾管理
    def setUp(self):
        User.objects.create_user(username='admin',password='111111',email='admin@qq.com')
        Event.objects.create(id=1, name="xiaomi7",
                             limit=2000, address='chengdu',
                             status=1,start_time='2019-2-22 12:30:00')
        Guest.objects.create(realname ='tong',phone =15181001129,
                             email ='836096322@qq.com',sign =False,
                             create_time =datetime(2019,2,22,14,0,0),event_id=1)
        login_user = {'username': 'admin', 'password': '111111'}
        self.client.post('/login_action/', data=login_user)  # 预先登录
    def test_guest_mange_success(self):
        #测试嘉宾信息获取
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b"836096322@qq.com",response.content)
        self.assertIn(b"tong", response.content)
    def test_guest_mange_search_success(self):
        #测试嘉宾信息搜索
        response = self.client.get('/search_phone/',{'phone':'15181001129'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"tong",response.content)
        self.assertIn(b"15181001129", response.content)
class SignIndexActionTest(TestCase):
    #发布会签到
    def setUp(self):
        User.objects.create_user(username='admin',password='111111',email='admin@qq.com')
        Event.objects.create(id=1, name="xiaomi7",
                             limit=20, address='chengdu',
                             status=1,start_time='2019-2-22 12:30:00')
        Event.objects.create(id=2, name="xiaomi8",
                             limit=20, address='beijin',
                             status=1, start_time='2019-2-22 12:30:00')
        Guest.objects.create(realname ='tong',phone =15181001129,
                             email ='836096322@qq.com',sign =False,
                             create_time =datetime(2019,2,22,14,0,0),event_id=1)
        Guest.objects.create(realname='alenwang', phone=15181001523,
                             email='836096322@qq.com', sign=True,
                             create_time=datetime(2019, 2, 22, 14, 0, 0), event_id=2)
        login_user = {'username': 'admin', 'password': '111111'}
        self.client.post('/login_action/', data=login_user)  # 预先登录
    def test_sign_index_action_phone_error(self):
        #手机号错误
        response = self.client.post('/sign_index_action/1/',{"phone": "dfdsdf"})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"phone error",response.content)
    def test_sign_index_action_phone_not_event_id_list(self):
        #手机号不在签到列表
        response = self.client.post('/sign_index_action/1/',{'phone':'15181001523'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"phone is not on the current release list",response.content)
    def test_sign_index_action_user_sign_has(self):
        #手机号已签到
        response = self.client.post('/sign_index_action/2/',{'phone':'15181001523'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"The user has checked in",response.content)
    def test_sign_index_action_sign_success(self):
        #签到成功
        response = self.client.post('/sign_index_action/1/',{'phone':'15181001129'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"Sign in successfully",response.content)