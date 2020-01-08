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

@csrf_exempt
def add_guest(request):
    html = ''
    try:
        ospiteOBJ = base.Ospite(
            utente=request.COOKIES['hash'],
        )
        ospiteOBJ.save()
        diz_html = costants.def_usr_data
        diz_html['id_ospite'] = ospiteOBJ.id_ospite
        html = view.render_aggiungi_ospite(diz_html)
    except:
        print(traceback.format_exc())
        html = traceback.format_exc()
    return HttpResponse(html)



@csrf_exempt
def update_guest(request):
    res = 'KO'
    try:
        ospiteOBJ = base.Ospite.objects.get(
                id_ospite=request.POST['id_ospite']
            )
        ospiteOBJ.__setattr__(request.POST['campo'], request.POST['valore'])
        ospiteOBJ.save()

        res = 'OK'#{campo} aggiornato con {valore}'.format(**request.POST)
    except:
        print(traceback.format_exc())
    return HttpResponse(res)


@csrf_exempt
def delete_guest(request):
    try:
        ospiteOBJ = base.Ospite(
                id_ospite=request.POST['id_ospite']
            )
        ospiteOBJ.delete()
    except:
        print(traceback.format_exc())
    return HttpResponse('ok')

@csrf_exempt
def get_image(request):
    filename = (request.META['PATH_INFO'].split('/')).pop()
    with open(settings.IMAGE_USER_PATH + filename , 'r') as content_file:
        content = content_file.read()
    return HttpResponse(content)

@csrf_exempt
def check_login(request):
    ret = HttpResponse()
    utenteOBJ = base.Famiglia.objects.filter(
        hash=request.POST['hash_inserito']
    )
    if utenteOBJ:
        ret.set_cookie('hash', utenteOBJ[0].hash)
        ret.set_cookie('login', True)
        ret.content = 'ok'
        #HttpResponseRedirect("%s/html/" % settings.APPSERVER)
    else:
        ret.delete_cookie('hash')
        ret.set_cookie('login', False)
        ret.content = 'ko'
    return ret


@csrf_exempt
def save_image(request):
    stream = request.FILES['image']
    nome_file = request.COOKIES['hash']
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

    ospiteOBJ = base.Ospite.objects.get(
        id_ospite=request.POST['id_ospite']
    )
    ospiteOBJ.url_img_user = settings.IMAGE_USER_PATH_RELATIVE + nome_file
    ospiteOBJ.save()

    return ret

def debug_request(input):
    pprint.pprint(input.__dict__, width=160)