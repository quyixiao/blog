from django.conf.urls import url
from .views import reg
from .views import login,test

urlpatterns = [
    url(r'^reg$', reg),
    url(r'^login$', login),
    url(r'^test$', test),

]
