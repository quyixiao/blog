import bcrypt
from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseBadRequest, Http404, HttpResponseNotFound
import json

from user.models import User
import logging
import simplejson
from django.conf import settings
import jwt

import datetime

# 根logging 如果没有创建的话，
FORMAT = '%(asctime)s 【%(levelname)s】 [%(filename)s:%(lineno)d] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

AUTH_EXPIRE = 60 * 60 * 8


def checkemail(request: HttpRequest):
    # 判断email
    return True


def get_token(user_id):
    return jwt.encode({'user_id': user_id, 'exp': int(datetime.datetime.now().timestamp()) + AUTH_EXPIRE},
                      settings.SECRET_KEY,
                      'HS256').decode()


def reg(request: HttpRequest):
    print(type(request))
    print(request.GET)
    print(request.POST)
    try:
        try:
            # qs = User.objects.get(pk=1) #  User matching query does not exist.,当主键没有12的时候抛出这个异常
            # qs = User.objects.filter(pk=1).all()
            qs = User.objects.filter(pk__lte=1).all()
            print(qs.query)
            print(qs)
        except Exception as e:
            logging.error(e)
        finally:
            print('*' * 30)

        data = simplejson.loads(request.body)
        logging.info(data)
        # 数据中email 有没有，如果有和话，则直接抛出异常
        user = User()
        user.name = data['name']
        user.email = data['email']
        password = data['password']
        user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        qs = User.objects.filter(email=user.email)  # <class 'django.db.models.manager.Manager'>

        print(qs.query)
        print(type(qs))  # 查询级别
        print(qs)
        if qs:  # 如果Email 已经存在了
            return HttpResponseBadRequest()
        print(user.password)

        user.save()
        return JsonResponse({"token": get_token(user.id)})

    except Exception as e:
        logging.error(e)
        return HttpResponseBadRequest()
    finally:
        pass
    return JsonResponse({'d': 'abc'})


def login(request: HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        password = payload['password']
        print(email)
        print(password)
        user = User.objects.filter(email=email).get()
        if not user:
            logging.info('not user ')
            return HttpResponseBadRequest()
        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            logging.info('password exception ')
            return HttpResponseBadRequest()
        token = get_token(user.id)
        res = JsonResponse({'user': {
            'user_id': user.id,
            'name': user.name,
            'email': user.email
        }, 'token': token
        })
        res.set_cookie('Jwt', token)
        logging.info(res)
        return res
    except Exception as e:
        logging.error(e)
    return JsonResponse({'code': 9999})


def authenticate(view):
    def wapper(request: HttpRequest):
        # 提取出用户提交的
        token = request.META.get('HTTP_JWT')
        logging.info('用户登陆：' + token)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')  # 时间自动较验
            request.user = User.objects.filter(pk=payload['user_id']).get()
            return view(request)
        except Exception as e:
            logging.error(e)
        return JsonResponse({'code': 9999})

    return wapper


@authenticate
def test(request: HttpRequest):
    print("test")
    user = request.user
    logging.info('user_id ' + str(user.id))
    return JsonResponse({'code': 200})
