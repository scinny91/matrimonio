import pprint
import random
import codecs
import os


from . import costants
from .bo import base
from matrimonio import settings


def render_index(diz_html):
    diz_html['menu'] = render_menu(diz_html)
    with codecs.open(settings.STATIC_HTML + '/html/index.html', 'r', encoding='utf-8', errors='ignore') as content_file:
        html = content_file.read()
    html = html.format(**diz_html)
    return html


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

def render_info(diz_html):
    with codecs.open(settings.STATIC_HTML + '/html/info.html', 'r', encoding='utf-8', errors='ignore') as content_file:
        html = content_file.read()
    html = html.format(**diz_html)
    return html


def render_profilazione(diz_html):
    with codecs.open(settings.STATIC_HTML + '/html/profilazione.html', 'r', encoding='utf-8', errors='ignore') as content_file:
        html = content_file.read()
    html = html.format(**diz_html)
    return html

def render_unauth(diz_html):
    with codecs.open(settings.STATIC_HTML + '/html/unauthorized.html', 'r', encoding='utf-8', errors='ignore') as content_file:
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
                 <td class="cella_ospiti title"> Sesso </td> 
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
                                    <td class="cella_ospiti"> {sesso} </td> 
                                    <td class="cella_ospiti"> {albergo} </td>
                                    <td class="cella_ospiti"> {speciale} </td>  
                                    <td class="cella_ospiti"> {upd_ts} </td> 
                                   </tr>'''.format(**ospite))
            #print(ospite)
        lista_html.append('<tr class="famiglia"> <td colspan=5> <table class="tabella_ospiti"> %s </table> </td> </tr>' % ''.join(tabella_ospiti))
    lista_html.append('</table>')

    return ''.join(lista_html)

def render_riga_invitato(famiglia, invitato):
    riga = costants.blocco_righe_invitato
    invitato['mostra_albergo'] = ''
    if famiglia.albergo_abilitato != 'S':
        invitato['mostra_albergo'] = 'nascosta'
    return riga.format(**invitato)


def render_menu(diz_html):
    lista_pulsanti = []
    if diz_html['page'] != 'index':
        lista_pulsanti.append("""<li class='pulsanti_menu'><a href="{appserver}" class="btn btn-round btn-block ">Home</a></li>""")
    if diz_html['page'] != 'profilazione':
        lista_pulsanti.append("""<li  class='pulsanti_menu'><a href="{appserver}/profilazione/" class="btn btn-round btn-block ">Profilazione</a></li>""")
    if diz_html['page'] != 'info':
        lista_pulsanti.append("""<li  class='pulsanti_menu'><a href="{appserver}/info/" class="btn btn-round btn-block pulsanti_menu">Info</a></li>""")
    if diz_html['page'] != 'admin' and diz_html['hash'] == 'super_user':
        lista_pulsanti.append("""<li  class='pulsanti_menu'><a href="{appserver}/admin/" class="btn btn-round btn-block ">Admin</a></li>""")
    lista_pulsanti.append("""<li  class='pulsanti_menu'><a onclick="logout()" class="btn btn-round btn-block ">Logout</a></li>""")

    diz_html['pulsanti'] = ''.join(lista_pulsanti).format(**diz_html)


    html = """
    <div class="container">
        <nav class="navbar navbar-ct-blue navbar-transparent navbar-fixed-top" role="navigation">

          <div class="container">
            <!-- Brand and toggle get grouped for better mobile display -->
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>

                     <div class="logo-container">
                        <div class="logo">
                            <img src="{appserver}/assets/img/new_logo.png">
                        </div>
                        <div class="brand">

                            Mancano: {delta_days} giorni!
                        </div>
                    </div>
            </div>

            <!-- Collect the nav links, forms, and other content for toggling -->
            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
              <ul class="nav navbar-nav navbar-right">
                    {pulsanti}
               </ul>

            </div><!-- /.navbar-collapse -->
          </div><!-- /.container-fluid -->
        </nav>
    </div><!--  end container-->
    """.format(**diz_html)
    return html

def html_carosello(tipo_carosello, rand=True):
    html = []

    DIR = settings.IMG_DIR + '/%s/' % tipo_carosello

    uuid = os.listdir(DIR)
    if rand:
        random.shuffle(uuid)
    for name in uuid:
        if '.jpeg' in name:
            selected = '' if name != 'foto1.jpeg' else 'active'
            html.append("""
            <div class="item {selected}">
                <img src="assets/img/{tipo_carosello}/{name}" alt="{name}">
            </div>
            """.format(**locals()))


    return ''.join(html)