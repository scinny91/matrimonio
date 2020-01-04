"""matrimonio URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from .backand import start, controller

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^html/', start.start),
    url(r'^/img_user/', controller.get_image),
    url(r'^controller/', controller.main),
    url(r'^save_image/', controller.save_image),
    url(r'^delete_guest/', controller.delete_guest),
    url(r'^update_guest/', controller.update_guest),
    url(r'^add_guest/', controller.add_guest),
]
