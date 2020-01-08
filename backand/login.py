from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .bo import base
from . import view, start, costants
from matrimonio import settings


def mostra_login(request):
    crea_hash()
    ret = HttpResponse()
    if not request.COOKIES.get('login') and request.META['PATH_INFO'] == '/':
        # login non fatto o fallito
        ret.content = render_login(ret)
    else:
        # file statici, richiamo start
        ret = start.get_statics_file(request)
    return ret


def render_login(ret):
    diz_html = {
        'appserver': settings.APPSERVER,
        'delta_days': costants.delta_days,
        'due_date_umana': costants.due_date_umana,
        'js_index': costants.js_index,
    }
    return view.render_login(diz_html)


def crea_hash():
    elenco_famiglie = base.Famiglia.objects.filter()

    for famiglia in elenco_famiglie:
        if not famiglia.hash:
            famiglia.calcola_hash()