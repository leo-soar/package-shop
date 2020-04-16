import hashlib
import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from user.models import UserProfile
from dtoken.views import Tokens

class Users(View):

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


        return JsonResponse({'code':200,'data':{'token':token.decode()},'carts_count':0})

