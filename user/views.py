import base64
import hashlib
import json
import random

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render

from django.views import View
from user.models import UserProfile
from dtoken.views import Tokens
# Create your views here.

class Users(View):

    def send_active_email(self,email_address,v_url):
        #发激活邮件
        subject = '达达商城激活邮件'
        html_message = '''
        <p>尊敬的用户您好</p>
        <p>请点击此链接激活您的账户(3天内有效):</p>
        <p><a href='%s' target='_blank'>点击激活</a></p>
        '''%v_url
        send_mail(subject,'',from_email=settings.EMAIL_HOST_USER,recipient_list=[email_address],html_message=html_message)


    def dispatch(self, request, *args, **kwargs):
        json_str = request.body
        json_obj = json.loads(json_str)
        request.json_obj = json_obj

        return super().dispatch(request, *args, **kwargs)
    # {"uname": "xiaonao", "password": "123456", "phone": "13323333443", "email": "dada@tedu.cn", "carts": null}

    def post(self,request):
        data = request.json_obj
        uname = data['uname']
        password = data['password']
        phone = data['phone']
        email = data['email']
        #TODO 参数判断
        old_users = UserProfile.objects.filter(username=uname)
        if old_users:
            return JsonResponse({'code':10101,'error':'Your username is already existed!'})

        m = hashlib.md5()
        m.update(password.encode())

        #创建用户
        try:
            user = UserProfile.objects.create(
                username=uname,password=m.hexdigest(),phone=phone,email=email
            )
        except Exception as e:
            print('-------create error is:',e)
            return JsonResponse({'code': 10102, 'error': 'Your username is already existed~~'})

        #生产令牌
        token = Tokens.make_token(uname)

        #校验链接中查询字符串
        #修改用户is_active 值
        try:
            #激活邮件 有效期3天 隐秘 send_mail
            #生成随机数
            code = '%s'%(random.randint(1000,9999))
            code_str = code + '_' + uname
            active_code = base64.urlsafe_b64encode(code_str.encode())
            cache.set('email_active_%s'%(uname),code,3600*24*3)
            verify_url = 'http://127.0.0.1:7000/dadashop/templates/active.html?code=%s'%active_code.decode()
            print(verify_url)
            #发邮件
            self.send_active_email(email,verify_url)

        except Exception as e:
            print('---active error---')
            print(e)

        return JsonResponse({'code': 200, 'data': {'token': token.decode()}, 'carts_count': 0})

class ActiveView(View):

    def get(self,request):

        code = request.GET.get('code')
        if not code:
            return JsonResponse({'code':10104,'error':'no code'})

        verify_code = base64.urlsafe_b64decode(code.encode()).decode()

        code,username = verify_code.split('_')
        old_code = cache.get('email_active_%s'%username)
        if not old_code:
            return JsonResponse({'code':10105,'error':'The link is invalid!'})
        if code != old_code:
            return JsonResponse({'code':10106,'error':'The link is invalid~~'})

        user = UserProfile.objects.get(username=username)
        print(user)
        user.is_active = True
        user.save()

        cache.delete('email_active_%s'%username)
        return JsonResponse({'code':200,'data':'ok'})

