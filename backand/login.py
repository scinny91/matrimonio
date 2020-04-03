from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from .bo import base, doc
from . import view, start, costants, controller
from matrimonio import settings
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

    return controller._check_login(hash_inserito, fromQr=True)


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
    elenco_famiglie = base.Famiglia.objects.filter()
    for famiglia in elenco_famiglie:
        uuid = famiglia.__dict__
        invitati = base.Ospite.objects.filter(utente=famiglia.hash)
        uuid['invitati'] = [i.__dict__ for i in invitati]
        dati_tabella.append(uuid)


    diz_html = {
        'appserver': settings.APPSERVER,
        'delta_days': costants.delta_days,
        'due_date_umana': costants.due_date_umana,
        'js_index': costants.js_index,
        'version': costants.get_version(),
        'hash': request.COOKIES['hash'],
        'tabella_ospiti': view.render_tabella_ospiti(dati_tabella),
        'page' : 'admin',
    }
    diz_html['menu'] = view.render_menu(diz_html)
    html = view.render_admin(diz_html)
    return HttpResponse(html)

@check_login
def render_info(request):
    diz_html = {
        'appserver': settings.APPSERVER,
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
    lista_righe = [view.render_riga_invitato(famiglia, i.toHtml()) for i in dati_ospiti]
    diz_html['index_blocco_righe_invitato'] = ''.join(lista_righe)

    famiglia = base.Famiglia.objects.filter(hash=utente)
    desc_fam = 'None'
    if famiglia:
        desc_fam = famiglia[0].alias
    diz_html['hash'] = 'famiglia: %s (%s)' % (desc_fam, utente)


    html = view.render_profilazione(diz_html)
    return HttpResponse(html)


@check_login
def render_gallery(request):
    diz_html = {
        'appserver': settings.APPSERVER,
        'delta_days': costants.delta_days,
        'due_date_umana': costants.due_date_umana,
        'js_index': costants.js_index,
        'version': costants.get_version(),
        'hash': request.COOKIES['hash'],
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