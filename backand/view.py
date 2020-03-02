import pprint
import codecs


from . import costants
from .bo import base
from matrimonio import settings


def mostra_utenti_salvati(cookies):
    utente = cookies.get('hash', 'undef')
    famiglia = base.Famiglia.objects.filter(hash=utente)[0]

    ret = costants.get_costants()

    dati_ospiti = base.Ospite.objects.filter(utente=utente)
    lista_righe = [render_riga_invitato(famiglia, i.toHtml()) for i in dati_ospiti]
    ret['index_blocco_righe_invitato'] = ''.join(lista_righe)

    famiglia = base.Famiglia.objects.filter(hash=utente)
    desc_fam = 'None'
    if famiglia:
        desc_fam = famiglia[0].alias
    ret['hash'] = 'famiglia: %s (%s)' % (desc_fam, utente)


    return ret


def render_aggiungi_ospite(utente, diz_html):
    famiglia = base.Famiglia.objects.filter(hash=utente)[0]
    return render_riga_invitato(famiglia, diz_html)


def render_login(diz_html):
    with codecs.open(settings.STATIC_HTML + '/html/login.html', 'r', encoding='utf-8', errors='ignore') as content_file:
        html = content_file.read()
    html = html.format(**diz_html)
    return html

def render_admin(diz_html):
    with codecs.open(settings.STATIC_HTML + '/html/admin.html', 'r', encoding='utf-8', errors='ignore') as content_file:
        html = content_file.read()
    html = html.format(**diz_html)
    return html

def render_tabella_ospiti(dati_tabella):
    lista_html = ['<table class="tabella_ospiti">']
    if not dati_tabella:
        lista_html.append('Nessuna famiglia trovata')
    else:
        lista_html.append('''
        <tr> 
            <td class="cella_ospiti title"> Alias </td> 
            <td class="cella_ospiti title"> hash </td> 
            <td class="cella_ospiti title"> Nome famiglia </td>  
            <td class="cella_ospiti title"> Albergo abilitato </td>  
            <td class="cella_ospiti title"> Upd TS </td> 
        </tr>''')
    for famiglia in dati_tabella:
        lista_html.append('''
            <tr> 
                <td  class="cella_ospiti"> {alias} </td> 
                <td  class="cella_ospiti"> {hash} </td> 
                <td  class="cella_ospiti"> {nome_famiglia}</td>  
                <td  class="cella_ospiti"> {albergo_abilitato}</td>  
                <td  class="cella_ospiti"> {upd_ts} </td> 
            </tr>
            '''.format(**famiglia))
        tabella_ospiti = []
        if not famiglia['invitati']:
            tabella_ospiti.append('<tr class="ospite title"> <td> nessun ospite registrato </td> </tr>')

        else:
            tabella_ospiti.append('''
                <tr>
                 <td class="cella_ospiti title"> foto </td>
                 <td class="cella_ospiti title"> Nome </td> 
                 <td class="cella_ospiti title"> Mail </td> 
                 <td class="cella_ospiti title"> Note </td> 
                 <td class="cella_ospiti title"> Menu </td> 
                 <td class="cella_ospiti title"> Viaggio </td> 
                 <td class="cella_ospiti title"> Albergo </td>
                 <td class="cella_ospiti title"> Speciale </td>  
                 <td class="cella_ospiti title"> Upd TS </td> 
                </tr>''')
        for ospite in famiglia['invitati']:
            tabella_ospiti.append('''
                                   <tr>
                                    <td class="cella_ospiti"> <img src='../{url_img_user}' class='img-piccola'> </td>
                                    <td class="cella_ospiti"> {nome} </td> 
                                    <td class="cella_ospiti"> {mail} </td> 
                                    <td class="cella_ospiti"> {note} </td> 
                                    <td class="cella_ospiti"> {menu} </td> 
                                    <td class="cella_ospiti"> {viaggio} </td> 
                                    <td class="cella_ospiti"> {albergo} </td>
                                    <td class="cella_ospiti"> {speciale} </td>  
                                    <td class="cella_ospiti"> {upd_ts} </td> 
                                   </tr>'''.format(**ospite))
            print(ospite)
        lista_html.append('<tr class="famiglia"> <td colspan=5> <table class="tabella_ospiti"> %s </table> </td> </tr>' % ''.join(tabella_ospiti))
    lista_html.append('</table>')

    return ''.join(lista_html)

def render_riga_invitato(famiglia, invitato):
    riga = costants.blocco_righe_invitato
    invitato['mostra_albergo'] = ''
    pprint.pprint(famiglia.__dict__)
    if famiglia.albergo_abilitato != 'S':
        invitato['mostra_albergo'] = 'nascosta'
    pprint.pprint(invitato)
    return riga.format(**invitato)