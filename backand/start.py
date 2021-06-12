# -*- coding: utf-8 -*-

from django.http import HttpResponse

from matrimonio import settings
from . import costants, view
from .bo import base
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
    elif '.html' in url: #2020 03 21 lo stacco
        # per l'html ci schiaffo dentro le costanti...
        html = read_file(url)
        cookies = request.COOKIES
        hash = cookies.get('hash')
        if hash:
            objFamiglia = base.Famiglia.objects.get(hash=cookies['hash'])
            if 'index.html' in url:
                diz_html = {
                    'appserver': settings.APPSERVER,
                    'delta_days': costants.delta_days,
                    'due_date_umana': costants.due_date_umana,
                    'js_index': costants.js_index,
                    'version': costants.get_version(),
                    'hash': cookies['hash'],
                    'nome_famiglia': objFamiglia.nome_famiglia,
                    'page': 'index',
                    'carosello_alto': view.html_carosello('carosello', limit=7),
                    'indicators_alto': view.indicators_carosello('carosello', 'carousel-example-generic', limit=7),
                    'foto_sposo': view.html_carosello('carosello_sposo', rand=False),
                    'foto_sposa': view.html_carosello('carosello_sposa', rand=False),
                    'foto_sposo_testimoni': view.html_carosello('carosello_sposo_testimoni', rand=False),
                    'foto_sposa_testimoni': view.html_carosello('carosello_sposa_testimoni', rand=False),
                }
                html = view.render_index(diz_html)
        elif cookies.get('login') == 'False':
            diz_html = {
                'appserver': settings.APPSERVER,
                'delta_days': costants.delta_days,
                'due_date_umana': costants.due_date_umana,
                'js_index': costants.js_index,
                'version': costants.get_version(),
            }
            html = view.render_login(diz_html)
        else:
            diz_html = {
                'appserver': settings.APPSERVER,
                'version': costants.get_version(),
            }
            html = view.render_unauth(diz_html)

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

#test commir to delete