from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse, Http404
from django.shortcuts import render


# Create your views here.


def pub(request: HttpRequest):
    return HttpResponse(b'pub')


def get(request: HttpRequest, id):
    print(id)
    return HttpResponse(b'get')


def getall(request: HttpRequest):
    return HttpResponse(b'getall')
