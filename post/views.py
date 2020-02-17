from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse, Http404
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
        return JsonResponse({'post_id':post.id})
    except Exception as e :
        logging.error(e)
    return HttpResponse(b'pub error')


def get(request: HttpRequest, id):
    try:
        post_id = int(id)


    except Exception as e:
        print(e)
        return HttpResponseBadRequest()

    return HttpResponse(b'get')


def getall(request: HttpRequest):
    return HttpResponse(b'getall')
