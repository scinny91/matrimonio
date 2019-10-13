from django.http import JsonResponse, HttpResponse
import traceback
from matrimonio import settings
import costants
from PIL import Image
from django.core.files.base import ContentFile
import json
import pprint
from django.views.decorators.csrf import csrf_exempt

global res
global utente

from django.contrib.auth.decorators import login_required

def check_login(input):

    def check(request):
        if request.getattr('COOKIES'):
            if not request.COOKIES.get('login'):
                raise Exception('Login rifiutato....')
            else:
                utente = request.COOKIES['utente']

    return check()


#@check_login()
def main(request):
    res = {
        'result': [],
        'errori': [],
        'warning': [],
        'logs': str(request.__dict__),
        'logs': '',
    }

    dump(request)
    try:
        if not request.COOKIES.get('login'):
            raise Exception('Login rifiutato....')
        else:
            utente = request.COOKIES['utente']
        action = request.POST.get('action', request.GET.get('action', ''))
        res['result'] = action

        if not action:
            raise ValueError('action non specificata, esco')

        import sys
        diz = {'logs': None}
        diz.update((request.POST).dict())
        diz.update((request.GET).dict())
        res['result'] = getattr(sys.modules[__name__], action)(diz)

    except Exception:
        res['warning'] = []
        res['result'] = []
        res['errori'] = traceback.format_exc()


    return JsonResponse(res)


def add_guest(diz_in):
    html = costants.blocco_righe_invitato

    diz_html = costants.def_usr_data
    diz_html['row_id'] = diz_in['index']
    return html.format(**diz_html)

def save_guest(diz_in):
    print diz_in
    return 'Ok'

@csrf_exempt
def get_image(request):
    dump(request.META['PATH_INFO'])
    filename = (request.META['PATH_INFO'].split('/')).pop()
    with open(settings.IMAGE_USER_PATH + filename , 'r') as content_file:
        content = content_file.read()
    return HttpResponse(content)

@csrf_exempt
def save_image(request):
    stream = request.FILES['image']
    nome_file = request.COOKIES['utente']
    nome_file += '_'+ request.FILES['image']._name


    img = open(settings.IMAGE_USER_PATH + nome_file, 'w')
    img.write(stream.read())
    img.close()

    im1 = Image.open(settings.IMAGE_USER_PATH + nome_file)
    height = width = 200
    im2 = im1.resize((width, height), Image.NEAREST)
    im2.save(settings.IMAGE_USER_PATH +'resized/'+ nome_file)


    return HttpResponse(settings.IMAGE_USER_PATH_RELATIVE + nome_file)

def dump(input):
    pprint.pprint(input)