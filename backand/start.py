
from django.http import HttpResponse
from django.contrib.staticfiles.templatetags import staticfiles


def start(request):

    url = request.META['PATH_INFO']

    html = ''
    if url == '/html/':
        with open('matrimonio/matrimonio/html/index.html', 'r') as content_file:
            html = content_file.read()
    else:
        with open('matrimonio/matrimonio/%s' % url, 'r') as content_file:
            html = content_file.read()
    if '.js' in url:
        return HttpResponse(html, content_type="application/x-javascript")
    elif '.css' in url:
        return HttpResponse(html, content_type="text/css")
    else:
       return HttpResponse(html)
