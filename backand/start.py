# -*- coding: utf-8 -*-

from django.http import HttpResponse

from matrimonio import settings
from . import costants, view
import traceback
import codecs
from PIL import Image

def start(request):
    url = request.META['PATH_INFO']

    if url == '/html/':
        url += 'index.html'

    if '.js' in url:
        html = read_file(url)
        return HttpResponse(html, content_type="application/x-javascript")
    elif '.css' in url:
        html = read_file(url)
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
    elif '.jpeg' in url:
        img = Image.open(settings.STATIC_HTML + url)
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response
    elif '.gif' in url:
        img = Image.open(settings.STATIC_HTML + url)
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response
    elif '.html' in url:
        # per l'html ci schiaffo dentro le costanti...
        html = read_file(url)
        cookies = request.COOKIES
        if 'index.html' in url:
            html = html.format(**view.mostra_utenti_salvati(cookies))

        ret = HttpResponse()
        ret.content = html
        return ret
    elif '.ttf' in url:
        html = read_file(url)
        return HttpResponse(html)
    elif '.woff' in url:
        html = read_file(url)
        return HttpResponse(html, content_type='application/x-font-woff')
    else:
        html = read_file(url)
        return HttpResponse(html)

def read_file(url):
    html = ''
    with codecs.open(settings.STATIC_HTML + url, 'r', encoding='utf-8', errors='strict') as content_file:
        try:
            html = content_file.read()
        except:
            print('file in errore: ' + settings.STATIC_HTML + url)
            print(traceback.format_exc())
            raise
    return html


def get_statics_file(request):
    if request.META['PATH_INFO'] != '/':
        request.META['PATH_INFO'] = '/html/' + request.META['PATH_INFO']
    else:
        request.META['PATH_INFO'] = '/html/'
    return start(request)