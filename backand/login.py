from django.http import HttpResponse
from django.shortcuts import render, redirect
from .bo import base, doc
from . import view, start, costants, controller
from matrimonio import settings



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

def admin(request):
    if not request.COOKIES.get('hash') == 'super_user':
        return HttpResponse('utente non autorizzato')
    crea_hash()
    crea_segnaposto()
    return HttpResponse('operazioni eseguite, passo e chiudo!')


def crea_hash():
    elenco_famiglie = base.Famiglia.objects.filter()
    for famiglia in elenco_famiglie:
        if not famiglia.hash:
            famiglia.calcola_hash()
        famiglia.genera_partecipazione()

def crea_segnaposto():
    elenco_ospiti = base.Ospite.objects.filter()
    print(elenco_ospiti)
    doc.genera_segnaposto([i.nome for i in elenco_ospiti])
    pass