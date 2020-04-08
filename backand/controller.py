from django.http import HttpResponse, FileResponse
import traceback
from matrimonio import settings
from datetime import datetime
from . import view, login
from PIL import Image, ExifTags
import zipfile
import os
from django.views.decorators.csrf import csrf_exempt

global res
global utente

from matrimonio.backand.bo import base


@csrf_exempt
@login.check_login
def add_guest(request):
    html = ''
    try:
        hash_famiglia = request.COOKIES['hash']
        ospiteOBJ = base.Ospite(
            utente=hash_famiglia,
        )
        ospiteOBJ.save()
        diz_html =ospiteOBJ.toHtml()
        html = view.render_aggiungi_ospite(hash_famiglia, diz_html)
    except:
        print(traceback.format_exc())
        html = traceback.format_exc()
    return HttpResponse(html)


@csrf_exempt
@login.check_login
def add_comment(request):
    html = ''
    try:
        hash_utente = request.COOKIES['hash']

        objCommento = base.Commento(
            famiglia=hash_utente,
            utente_commento=request.POST['utente_commento'],
            descrizione=request.POST['commento']
        )
        objCommento.save()

        commenti = []
        for i in base.Commento.objects.filter():
            info_ospite = base.Ospite.objects.filter(nome=i.utente_commento, utente=i.famiglia)
            if info_ospite:
                i.info_ospite = info_ospite[0].__dict__
            else:
                i.info_ospite = {}

            info_famiglia = base.Famiglia.objects.filter(hash=i.famiglia)
            if info_famiglia:
                i.info_famiglia = info_famiglia[0].__dict__
            else:
                i.info_famiglia = {}

            commenti.append(i.__dict__)

        objFamiglia = base.Famiglia.objects.get(hash=hash_utente)
        html = view.render_tabella_commenti(commenti, objFamiglia)
    except:
        print(traceback.format_exc())
        html = traceback.format_exc()
    return HttpResponse(html)


@csrf_exempt
@login.check_login
def update_guest(request):
    res = 'KO'
    try:
        ospiteOBJ = base.Ospite.objects.get(
                id_ospite=request.POST['id_ospite']
            )
        ospiteOBJ.__setattr__(request.POST['campo'], request.POST['valore'])
        if request.POST['campo'] == 'mail':
            ospiteOBJ.mail_valida = 'N'
        ospiteOBJ.save()

        res = 'OK'#{campo} aggiornato con {valore}'.format(**request.POST)
    except:
        print(traceback.format_exc())
        res = traceback.format_exc()
    return HttpResponse(res)


@csrf_exempt
@login.check_login
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
def check_login(request):
    hash_inserito = request.POST['hash_inserito']
    return login.make_login(hash_inserito, HttpResponse())


@csrf_exempt
@login.check_login
def gallery_save_image(request):
    for nome_file in request.FILES:
        stream = request.FILES[nome_file]
        img = open(settings.GALLERY_PATH + 'original/' + nome_file, 'wb')
        img.write(stream.read())
        img.close()

        _ruota_immagine(settings.GALLERY_PATH + 'original/' + nome_file)

        im1 = Image.open(settings.GALLERY_PATH + 'original/' + nome_file)
        basewidth = 200
        wpercent = (basewidth / float(im1.size[0]))
        hsize = int((float(im1.size[1]) * float(wpercent)))
        im2 = im1.resize((basewidth, hsize), Image.ANTIALIAS)
        im2.save(settings.GALLERY_PATH + 'miniature/' + nome_file)

        basewidth = 1280
        wpercent = (basewidth / float(im1.size[0]))
        hsize = int((float(im1.size[1]) * float(wpercent)))
        im3 = im1.resize((basewidth, hsize), Image.ANTIALIAS)
        im3.save(settings.GALLERY_PATH + 'ridimensionate/' + nome_file)


    ret = HttpResponse(view.get_elenco_file_gallery())

    return ret


@csrf_exempt
@login.check_login
def save_image(request):
    stream = request.FILES['image']
    nome_file = request.COOKIES['hash']

    estesione = stream._name.split('.').pop()
    nome_file += str(datetime.now()) #senno l'immagine cambia ma il browser se la cacha e mi fotte
    nome_file += '.'
    nome_file += estesione

    img = open(settings.IMAGE_USER_PATH +'original/' + nome_file, 'wb')
    img.write(stream.read())
    img.close()

    _ruota_immagine(settings.IMAGE_USER_PATH + 'original/' + nome_file)

    im1 = Image.open(settings.IMAGE_USER_PATH +'original/' + nome_file)
    height = width = 200
    im2 = im1.resize((width, height), Image.NEAREST)



    im2.save(settings.IMAGE_USER_PATH + nome_file)

    ret = HttpResponse('../' + settings.IMAGE_USER_PATH_RELATIVE + nome_file)
    ret.set_cookie('url_img_user', '../' + settings.IMAGE_USER_PATH_RELATIVE + nome_file)

    ospiteOBJ = base.Ospite.objects.get(
        id_ospite=request.POST['id_ospite']
    )
    ospiteOBJ.url_img_user = settings.IMAGE_USER_PATH_RELATIVE + nome_file
    ospiteOBJ.save()

    return ret


@login.check_login
def admin_download(request):
    if not request.COOKIES.get('hash') == 'super_user':
        return HttpResponse('utente non autorizzato')

    zf = zipfile.ZipFile("doc.zip", "w")
    for dirname, subdirs, files in os.walk(settings.DOCDIR):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()

    res = FileResponse(open("doc.zip", 'rb'), content_type='application/zip', filename='doc.zip')
    os.remove("doc.zip")
    return res


def _ruota_immagine(path):
    # la ruoto dal lato corretto
    try:
        image = Image.open(path)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
        image.save(path)
        image.close()
    except:
        image.close()
    # fine rotazione