import pprint
import codecs


from . import costants
from .bo import base
from matrimonio import settings


def mostra_utenti_salvati(cookies):
    ret = costants.get_costants()
    utente = cookies.get('hash', 'undef')
    dati_ospiti = base.Ospite.objects.filter(utente=utente)
    lista_righe = [(costants.blocco_righe_invitato).format(**i.toHtml()) for i in dati_ospiti]
    ret['index_blocco_righe_invitato'] = ''.join(lista_righe)

    famiglia = base.Famiglia.objects.filter(hash=utente)
    desc_fam = 'None'
    if famiglia:
        desc_fam = famiglia[0].alias
    ret['hash'] = 'famiglia: %s (%s)' % (desc_fam, utente)


    return ret


def render_aggiungi_ospite(diz_html):
    html = costants.blocco_righe_invitato
    return html.format(**diz_html)


def render_login(diz_html):
    with codecs.open(settings.STATIC_HTML + '/html/login.html', 'r', encoding='utf-8', errors='ignore') as content_file:
        html = content_file.read()
    html = html.format(**diz_html)
    return html