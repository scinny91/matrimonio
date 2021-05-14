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
from .backand import view, controller, login

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    #url(r'^html/', start.start),
    url(r'^save_image/', controller.save_image),
    url(r'^delete_guest/', controller.delete_guest),
    url(r'^update_guest/', controller.update_guest),
    url(r'^add_guest/', controller.add_guest),
    url(r'^add_comment/', controller.add_comment),
    url(r'^delete_comment/', controller.delete_comment),
    url(r'^check_login/', controller.check_login),
    url(r'^fast_login/', login.fast_login),
    url(r'^fl/', login.fast_login),
    url(r'^admin/', login.admin),
    url(r'^info/', login.render_info),
    url(r'^viaggio/', login.render_viaggio),
    url(r'^guestbook/', login.render_guestbook),
    url(r'^profilazione/', login.render_profilazione),
    url(r'^gallery/', login.render_gallery),
    url(r'^gallery_save_image/', controller.gallery_save_image),
    url(r'^admin_download/', controller.admin_download),
    url(r'', login.mostra_login),
]
