# -*- coding: utf-8 -*-

from django.http import HttpResponse

from matrimonio import settings
from . import costants
import traceback
import codecs
from PIL import Image

def start(request):
    url = request.META['PATH_INFO']

    html = ''
    if url == '/html/':
        url += 'index.html'

    with codecs.open(settings.STATIC_HTML + url, 'r', encoding='utf-8', errors='ignore') as content_file:
        try:
            html = content_file.read()
        except:
            print('file in errore: ' + settings.STATIC_HTML + url)
            print(traceback.format_exc())

    if '.js' in url:
        return HttpResponse(html, content_type="application/x-javascript")
    elif '.css' in url:
        return HttpResponse(html, content_type="text/css")
    elif '.png' in url:
        img = Image.open(settings.STATIC_HTML + url)
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response
    elif '.jpg' in url:
        img = Image.open(settings.STATIC_HTML + url)
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response
    elif '.html' in url:
        # per l'html ci schiaffo dentro le costanti...
        html = html.format(**costants.get_costants())
        ret = HttpResponse(html)
        ret.set_cookie('utente', 'devel')
        ret.set_cookie('login', True)
        return ret
    elif '.ttf' in url:
        return HttpResponse(html, content_type='text/html')
    elif '.woff' in url:
        return HttpResponse(html, content_type='text/html')
    else:
        raise
        return HttpResponse(html)


