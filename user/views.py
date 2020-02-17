from django.shortcuts import render

# Create your views here.


from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseBadRequest, Http404, HttpResponseNotFound
import json

from user.models import User
import logging
import simplejson
from django.conf import settings

def checkemail(request: HttpRequest):
    # 判断email
    return True


# 根logging 如果没有创建的话，
FORMAT = '%(asctime)s 【%(levelname)s】 [%(filename)s:%(lineno)d] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)


def get_token(user_id):
    j = simplejson.dumps({'user_id':user_id})
    

# 异常处理
# 出现获取输入框提交信息异常，就返回异常
# 查询邮箱存在，返回异常
# save()方法保存数据，有异常，则向外抛出，捕获返回异常
# 注意一点，Django的异常类继承处HttpResponse类，所以不能Raise，只能return
# 前端通过状态码判断是否成功
# Django 会为模型类提供一个objects对象，它是一个djanggo.db.models.manager.Manager类型，用于与数据库交互
# 当定义模型类的时候，没有指定管理器后，则Djanggo会为模型类提供一个objects的管理器
# 如果在模型类中手动指定处理器后，Django不再提供的objects的管理器了
# 对模型对象的CRUD ,被Django ORM 转换成相应的SQL 语句操作不同的数据源
# 对象 增加，修改，删除，查询 ，SQL insert ,update ,delete ,select
# 查询会返回结果集合，它是django,db.models.query.QuerySet集合类型
# 它是惰性求值，sqlalchemy一样，结果就是查询的集
# 它是可迭代的对象
# 惰性求值
# 创建查询集不会带来任何数据库的访问，直到调用数据时，都会访问数据库，可迭代序列化，if 语句中都会立即求值
# 缓存
# 每一个查询集都会包含一个缓存 ，来最小化对数据库的访问
# 新建查询集，缓存为空，首次对查询集求值时，会发生数据库的查询，Django 会把查询结果存在这个缓中，并返回请求的结果，接下来对
# 查询集合对象
# all()
# filter()          过滤，返回满足条件的数据
# exclude()         排队，排队满足条件的数据
# order_by()
# values()          返回一个对象的字典的列表，像json
# filter(k1=v1).filter(k2=v) 等价于filter(k1=v,k2=v)
# filter(pk=10) 这里pk批的就是主键，不用关心主键字段名，当然也是可以使用主键名filter(emp_no=10)
# 返回单个值的方法
# get()仅返回单个满足条件的对象，如果款能返回对象，则抛出DoseNotExist异常，如果能返回多条，抛出MultipleObjectReturned
# count() 返回当前查询的总条数
# fisrt()   返回每一个对象
# last() 返回最后的一个对象
# exist() 判断查询集中是否有数据，如果有则返回True
#
#


def reg(request: HttpRequest):
    print(request, '------------------')
    print(type(request))
    print(request.GET)
    print(request.POST)
    try:
        try:
            #qs = User.objects.get(pk=1) #  User matching query does not exist.,当主键没有12的时候抛出这个异常
            #qs = User.objects.filter(pk=1).all()
            qs = User.objects.filter(pk__lte=1).all()
            print(qs.query)
            print(qs)
        except Exception as e :
            logging.error(e)
        finally:
            print('*'*30)

        print('------------------------------------')
        data = simplejson.loads(request.body)
        logging.info(data)
        # 数据中email 有没有，如果有和话，则直接抛出异常
        user = User()
        user.name = data['name']
        user.email = data['email']
        user.password = data['password']

        qs = User.objects.filter(email=user.email)  # <class 'django.db.models.manager.Manager'>

        print(qs.query)
        print(type(qs))  # 查询级别
        print(qs)
        if qs:  # 如果Email 已经存在了
            return HttpResponseBadRequest()
        print(user.password)

        user.save()
        return JsonResponse({"user_id": user.id})

    except Exception as e:
        logging.error(e)
        return HttpResponseBadRequest()
    finally:
        pass
    return JsonResponse({'d': 'abc'})
