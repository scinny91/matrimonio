from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .bo import base
from . import view, start
from matrimonio import settings

import pprint

def login(request):
    #crea_hash()
    print(request.COOKIES)
    ret = HttpResponse()
    if not request.COOKIES.get('login'): #nulla di nulla
        ret.set_cookie('login', True)
        ret.set_cookie('hash', 'b5f4d1d047')
        ret.content = render_login(ret)
        print('primo giro, setto hash...')
    else: #qualcosa inserito
        check_login(ret)
        ret.set_cookie('login', True)
        #valida
        if False: # login errato
            pass
        else: #login corretto, procedo
            response = HttpResponseRedirect("%s/html/" % settings.APPSERVER)
            return response



    return ret


def render_login(ret):
    return 'finestra_login {hash}'.format(**ret.cookies)

def check_login(ret):
    print('valido login tramite hash presente nel cookies')
    return


def crea_hash():
    elenco_famiglie = base.Famiglia.objects.filter()

    for famiglia in elenco_famiglie:
        if not famiglia.hash:
            famiglia.calcola_hash()