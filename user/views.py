from django.shortcuts import render

# Create your views here.


from django.http import JsonResponse,HttpRequest,HttpResponse

def reg(request:HttpRequest):
    return JsonResponse({'d':'abc'})

