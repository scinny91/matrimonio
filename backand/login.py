from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .bo import base, doc
from . import view, start, costants, controller
from matrimonio import settings
import datetime
import random
import os


def check_login(func):
    def wrapper(request):
        if request.COOKIES.get('login'):
            return func(request)
        else:
            diz_html = {
                'appserver': settings.APPSERVER,
                'version': costants.get_version(),
            }
            return HttpResponse(view.render_unauth(diz_html))
    return wrapper


def mostra_login(request):
    ret = HttpResponse()
    if not request.COOKIES.get('login') and request.META['PATH_INFO'] == '/':
        # login non fatto o fallito
        ret.content = render_login(ret)
    else:
        # file statici, richiamo start
        ret = start.get_statics_file(request)
    return ret


def fast_login(request):
    hash_inserito = request.GET.get('hash', '')

    return make_login(hash_inserito, HttpResponseRedirect(settings.APPSERVER))


def render_login(ret):
    diz_html = {
        'appserver': settings.APPSERVER,
        'delta_days': costants.delta_days,
        'due_date_umana': costants.due_date_umana,
        'js_index': costants.js_index,
        'version': costants.get_version(),
    }
    return view.render_login(diz_html)


@check_login
def admin(request):
    if not request.COOKIES.get('hash') == 'super_user':
        return HttpResponse('utente non autorizzato')

    dati_tabella = []
    ospiti = []
    elenco_famiglie = base.Famiglia.objects.filter()
    import operator
    for famiglia in sorted(elenco_famiglie, key=operator.attrgetter('nome_famiglia')):
        uuid = famiglia.__dict__
        invitati = base.Ospite.objects.filter(utente=famiglia.hash)
        uuid['invitati'] = [i.__dict__ for i in invitati]
        dati_tabella.append(uuid)
        ospiti.extend(invitati)



    diz_html = {
        'appserver': settings.APPSERVER,
        'delta_days': costants.delta_days,
        'due_date_umana': costants.due_date_umana,
        'js_index': costants.js_index,
        'version': costants.get_version(),
        'hash': request.COOKIES['hash'],
        'tabella_ospiti': view.render_tabella_ospiti(dati_tabella),
        'famiglie': len(elenco_famiglie),
        'ospiti': len(ospiti),
        'maschi': len([i for i in ospiti if i.sesso == 'Uomo']),
        'femmine': len([i for i in ospiti if i.sesso == 'Donna']),
        'bambini': len([i for i in ospiti if i.menu == 'bambino']),
        'page': 'admin',
    }
    diz_html['menu'] = view.render_menu(diz_html)
    html = view.render_admin(diz_html)
    return HttpResponse(html)


@check_login
def render_info(request):
    objFamiglia = base.Famiglia.objects.get(hash=request.COOKIES['hash'])
    diz_html = {
        'appserver': settings.APPSERVER,
        'nome_famiglia': objFamiglia.nome_famiglia,
        'delta_days': costants.delta_days,
        'due_date_umana': costants.due_date_umana,
        'js_index': costants.js_index,
        'version': costants.get_version(),
        'hash': request.COOKIES['hash'],
        'page': 'info',
    }
    diz_html['menu'] = view.render_menu(diz_html)
    html = view.render_info(diz_html)
    return HttpResponse(html)


@check_login
def render_viaggio(request):
    objFamiglia = base.Famiglia.objects.get(hash=request.COOKIES['hash'])
    diz_html = {
        'appserver': settings.APPSERVER,
        'nome_famiglia': objFamiglia.nome_famiglia,
        'delta_days': costants.delta_days,
        'due_date_umana': costants.due_date_umana,
        'js_index': costants.js_index,
        'version': costants.get_version(),
        'hash': request.COOKIES['hash'],
        'page': 'viaggio',
        'tabella_nozze': view.render_tabella_lista_nozze(base.ListaNozze.objects.exclude(stato='annullato')),
    }
    diz_html['menu'] = view.render_menu(diz_html)

    html = view.render_lista_nozze(diz_html)
    return HttpResponse(html)


@check_login
def render_guestbook(request):
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

    utente = request.COOKIES['hash']
    dati_utente = base.Ospite.objects.filter(utente=utente)
    objFamiglia = base.Famiglia.objects.get(hash=utente)

    diz_html = {
        'appserver': settings.APPSERVER,
        'nome_famiglia': objFamiglia.nome_famiglia,
        'delta_days': costants.delta_days,
        'due_date_umana': costants.due_date_umana,
        'js_index': costants.js_index,
        'version': costants.get_version(),
        'hash': request.COOKIES['hash'],
        'page': 'guestbook',
        'sezione_commenti': view.render_tabella_commenti(commenti, objFamiglia),
        'nuovo_commento': view.render_nuovo_commento(dati_utente),
    }
    diz_html['menu'] = view.render_menu(diz_html)
    html = view.render_guestbook(diz_html)
    return HttpResponse(html)


@check_login
def render_profilazione(request):
    diz_html = {
        'appserver': settings.APPSERVER,
        'delta_days': costants.delta_days,
        'due_date_umana': costants.due_date_umana,
        'js_index': costants.js_index,
        'version': costants.get_version(),
        'hash': request.COOKIES['hash'],
        'page': 'profilazione',
    }
    diz_html['menu'] = view.render_menu(diz_html)

    utente = request.COOKIES['hash']
    famiglia = base.Famiglia.objects.filter(hash=utente)[0]
    dati_ospiti = base.Ospite.objects.filter(utente=utente)
    lista_righe = [view.render_blocco_righe_invitato(i.toHtml(famiglia)) for i in dati_ospiti]
    diz_html['nome_famiglia'] = famiglia.nome_famiglia
    diz_html['index_blocco_righe_invitato'] = ''.join(lista_righe)
    if not lista_righe:
        diz_html['index_blocco_righe_invitato'] = '''
         <div class="row" id='scritta_vuota'>
            <div class="col-sm-2"></div>
            <div class="col-sm-8">
                <h1>Nessun ospite registrato</h1>
            </div>
            <div class="col-sm-2"></div>
        </div>
        '''
    html = view.render_profilazione(diz_html)
    return HttpResponse(html)


@check_login
def render_gallery(request):
    objFamiglia = base.Famiglia.objects.get(hash=request.COOKIES['hash'])

    diz_html = {
        'appserver': settings.APPSERVER,
        'delta_days': costants.delta_days,
        'due_date_umana': costants.due_date_umana,
        'js_index': costants.js_index,
        'version': costants.get_version(),
        'hash': request.COOKIES['hash'],
        'nome_famiglia': objFamiglia.nome_famiglia,
        'page': 'gallery',
    }
    diz_html['menu'] = view.render_menu(diz_html)

    DIR = settings.IMG_DIR + '/gallery/original'
    elenco_file = os.listdir(DIR)
    elenco_file = [i for i in elenco_file if i != '.DS_Store']
    random.shuffle(elenco_file)
    diz_html['carosello'] = view.crea_html_carosello(elenco_file, '../assets/img/gallery/ridimensionate')
    diz_html['indicators_carosello'] = view.indicators_carosello('/gallery/original', 'carousel-example-generic')

    diz_html['elenco_file'] = view.get_elenco_file_gallery()

    html = view.render_gallery(diz_html)
    return HttpResponse(html)



def make_login(hash_inserito, response):
    codice_famiglia = None

    #fallback con codice utente
    famigliaObj = base.Famiglia.objects.filter(
        hash=hash_inserito
    )
    if famigliaObj:
        famigliaObj = base.Famiglia.objects.get(
            hash=hash_inserito
        )
        codice_famiglia = famigliaObj.hash
        famigliaObj.upd_ts = datetime.datetime.now()
        famigliaObj.save()
    else:
        ospiteObj = base.Ospite.objects.filter(
            nome=hash_inserito
        )
        if ospiteObj:
            codice_famiglia = ospiteObj[0].utente
            famigliaObj = base.Famiglia.objects.get(
                hash=codice_famiglia
            )
            famigliaObj.upd_ts = datetime.datetime.now()
            famigliaObj.save()

    if codice_famiglia:
        response.set_cookie('hash', codice_famiglia)
        response.set_cookie('login', True)
        response.content = 'ok'
    else:
        response.delete_cookie('hash')
        response.set_cookie('login', False)
        response.content = 'ko'
    return response


