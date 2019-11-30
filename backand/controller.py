from django.http import JsonResponse, HttpResponse
import traceback
from matrimonio import settings
from datetime import datetime
from . import costants, view
from PIL import Image
import hashlib
import json
import pprint
from django.views.decorators.csrf import csrf_exempt

global res
global utente

from matrimonio.backand.bo import base


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

    #debug_request(request)
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


def add_guest(request):
    html = view.render_aggiungi_ospite()
    return HttpResponse(html)

@csrf_exempt
def save_guest(request):
    #debug_request(request)

    try:
        dati_ospiti = json.loads(request.POST['lista_valori'])
        #pprint.pprint(dati_ospiti)
        for ospite in dati_ospiti:
            ospite['cod_famiglia'] = request.COOKIES['cod_famiglia']
            ospiteOBJ = base.Ospite(
                id_ospite=ospite.get('id_ospite'),
                nome=ospite['nome_ospite'],
                albergo=ospite['albergo'],
                bambino=ospite['bambino'],
                viaggio=ospite['viaggio'],
                menu=ospite['menu'],
                note=ospite['note'],
                url_img_user=ospite['url_img_user'],
                utente=ospite['cod_famiglia'],
                cod_famiglia=ospite['cod_famiglia'],
            )
            ospiteOBJ.save()
    except:
        print(traceback.format_exc())
    return HttpResponse('ok')

@csrf_exempt
def get_image(request):
    debug_request(request.META)
    filename = (request.META['PATH_INFO'].split('/')).pop()
    with open(settings.IMAGE_USER_PATH + filename , 'r') as content_file:
        content = content_file.read()
    return HttpResponse(content)

@csrf_exempt
def save_image(request):
    stream = request.FILES['image']
    nome_file = request.COOKIES['utente']
    nome_file += '_'+ request.FILES['image']._name
    estesione = nome_file.split('.').pop()

    img = open(settings.IMAGE_USER_PATH +'original/' + nome_file, 'wb')
    img.write(stream.read())
    img.close()

    im1 = Image.open(settings.IMAGE_USER_PATH +'original/' + nome_file)
    height = width = 200
    im2 = im1.resize((width, height), Image.NEAREST)


    nome_file = hashlib.md5(stream.read()).hexdigest()
    nome_file += str(datetime.now()) #senno l'immagine cambia ma il browser se la cacha e mi fotte
    nome_file += '.'
    nome_file += estesione

    im2.save(settings.IMAGE_USER_PATH + nome_file)

    ret = HttpResponse(settings.IMAGE_USER_PATH_RELATIVE + nome_file)
    ret.set_cookie('url_img_user', settings.IMAGE_USER_PATH_RELATIVE + nome_file)

    return ret

def debug_request(input):
    pprint.pprint(input.__dict__, width=160)