import math

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse, Http404, HttpResponseNotFound
import logging
import simplejson

import datetime

# 根logging 如果没有创建的话，
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


# /post?page=1
def getall(request: HttpRequest):
    try:
        page = int(request.GET['page'])
        size = int(request.GET['size'])
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
                'pages': math.ceil(count/size)
            }
        })
    except Exception as e:
        print(e)
    return HttpResponse(b'sucess')
