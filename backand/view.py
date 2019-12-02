from django.db.models import Max

from . import costants
from .bo import base

def mostra_utenti_salvati(cod_famiglia):
    ret = costants.get_costants()

    if cod_famiglia:
        dati_ospiti = base.Ospite.objects.filter(cod_famiglia=cod_famiglia)
        lista_righe = [(costants.blocco_righe_invitato).format(**i.__dict__) for i in dati_ospiti]
        ret['index_blocco_righe_invitato'] = ''.join(lista_righe)

    else:
        pass
        # index_blocco_righe_invitato e'  gia' caricato
        #html = costants.get_costants()

    return ret


def render_aggiungi_ospite():
    html = costants.blocco_righe_invitato
    diz_html = costants.def_usr_data
    diz_html['id_ospite'] = 1
    if base.Ospite.objects.aggregate(Max('id_ospite'))['id_ospite__max']:
        diz_html['id_ospite'] += base.Ospite.objects.aggregate(Max('id_ospite'))['id_ospite__max']
    return html.format(**diz_html)