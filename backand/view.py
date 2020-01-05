import pprint

from . import costants
from .bo import base

def mostra_utenti_salvati(cod_famiglia):
    ret = costants.get_costants()

    if cod_famiglia:
        dati_ospiti = base.Ospite.objects.filter(cod_famiglia=cod_famiglia)
        lista_righe = [(costants.blocco_righe_invitato).format(**i.toHtml()) for i in dati_ospiti]
        ret['index_blocco_righe_invitato'] = ''.join(lista_righe)

    else:
        pass
    return ret


def render_aggiungi_ospite(diz_html):
    html = costants.blocco_righe_invitato
    return html.format(**diz_html)