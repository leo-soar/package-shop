import hashlib
import json
import time
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from user.models import UserProfile

# Create your views here.


class Tokens(View):

    def dispatch(self, request, *args, **kwargs):
        json_str = request.body
        json_obj = json.loads(json_str)
        request.json_obj = json_obj

        return super().dispatch(request, *args, **kwargs)

    def post(self,request):
        data = request.json_obj
        username = data['username']
        password = data['password']
        #TODO 校验参数
        old_users = UserProfile.objects.filter(username=username)
        if not old_users:
            result = {'code':10201,'error':'The username or password is wrong!'}
            return JsonResponse(result)

        user = old_users[0]
        m = hashlib.md5()
        m.update(password.encode())
        if m.hexdigest() != user.password:
            result = {'code': 10202, 'error': 'The username or password is wrong~~'}
            return JsonResponse(result)

        #签发token
        token = self.make_token(username)

        result = {'code':200,'username':username,'data':{'token':token.decode()},'carts_count':0}
        return JsonResponse(result)

    def make_token(username, exp=3600 * 24):
        now = time.time()
        payload = {'username':username,'exp':now + exp}
        return jwt.encode(payload,settings.JWT_TOKEN_KEY,algorithm='HS256')
