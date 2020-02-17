"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# 模板
# 如果使用了react实现前端页面，其实Django就没有必要使用模板，它其实就是一个后台服务程序，接收请求，响应数据，接口设计就是可以纯粹的
# restful风格
# 模板的目的就是为可视化，将数据按照一定的布局格式输出，而不是为了处理数据，所以一般会有复杂的处理逻辑，模板的引入实现业务数据逻辑和显示
# 格式分离，这样，在开发中，就可分工协作了，页面开发完成页面的布局设计，后台开发完成数据处理逻辑实现，做的最多的是分工和迭代。
# Python 的模板引擎默认使用Django template language(DTL)) 构建
# 模板配置
# 在Settting.py 中设置模板项目的路径
# 点号的查的，
#

from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('user.urls')),
    url(r'^post/', include('post.urls'))
]
