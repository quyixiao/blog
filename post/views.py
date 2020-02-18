import math

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse, Http404, HttpResponseNotFound
import logging
import simplejson

import datetime

# 根logging 如果没有创建的话，分层，负责显示数据，每一个React组件xxx.js
# 服务层，钢表业务数据处理逻辑，命名为xxxService.js
# Model 层，负责数据，从数据后端取
#
from post.models import Post, Content
from user.views import authenticate

FORMAT = '%(asctime)s 【%(levelname)s】 [%(filename)s:%(lineno)d] %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)


# Create your views here.

@authenticate
def pub(request: HttpRequest):
    try:
        payload = simplejson.loads(request.body)

        post = Post()
        post.title = payload['title']
        post.author = request.user
        post.pubdate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        post.save()

        content = Content()
        content.content = payload['content']
        content.post = post
        content.save()
        return JsonResponse({'post_id': post.id})
    except Exception as e:
        logging.error(e)
    return HttpResponse(b'pub error')


def get(request: HttpRequest, id):
    try:
        post = Post.objects.get(pk=int(id))
        return JsonResponse({'post': {
            'post_id': post.id,
            'title': post.title,
            'content': post.content.content,
            'pubdate': int(post.pubdate.timestamp()),
            'author_id': post.author.id,
            'author': post.author.name
        }})
    except Exception as e:
        print(e)

    return HttpResponseNotFound(b'get')


def validate(d: dict, name, fn, default, val_fun=lambda x, y: x if x > 0 else y):
    try:
        ret = fn(d.get(name, default))
        return val_fun(ret, default)
    except Exception as e:
        logging.error(e)
    return default


# /post?page=1
def getall(request: HttpRequest):
    try:
        page = validate(request.GET, 'page', int, 1, lambda x, y: x if x > 0 else y)
        size = validate(request.GET, 'size', int, 20, lambda x, y: x if x > 0 and x < 101 else y)

        start = (page - 1) * size
        qs = Post.objects
        posts = qs.order_by('-id')[start:start + size]
        count = qs.count()

        print(posts.query)
        return JsonResponse({'posts': [{
            'post_id': post.id,
            'title': post.title,
            'pubdate': int(post.pubdate.timestamp()),
            'author': post.author.name
        } for post in posts],
            'pagination': {
                'page': page,
                'size': size,
                'totalCount': count,
                'pages': math.ceil(count / size)
            }
        })
    except Exception as e:
        print(e)
    return HttpResponse(b'sucess')
