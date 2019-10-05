from django.http import HttpResponse


from matrimonio import settings
import costants

def start(request):

    url = request.META['PATH_INFO']

    html = ''
    if url == '/html/':
        url += 'index.html'

    with open(settings.STATIC_HTML + url, 'r') as content_file:
        html = content_file.read()

    if '.js' in url:
        return HttpResponse(html, content_type="application/x-javascript")
    elif '.css' in url:
        return HttpResponse(html, content_type="text/css")
    elif '.html' in url:
        # per l'html ci schiaffo dentro le costanti...
        html = html.format(**costants.get_costants())
        return HttpResponse(html)
    else:
       return HttpResponse(html)


