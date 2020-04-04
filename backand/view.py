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


def render_gallery(diz_html):
    with codecs.open(settings.STATIC_HTML + '/html/gallery.html', 'r', encoding='utf-8', errors='ignore') as content_file:
        html = content_file.read()
    html = html.format(**diz_html)
    return html

def render_unauth(diz_html):
    with codecs.open(settings.STATIC_HTML + '/html/unauthorized.html', 'r', encoding='utf-8', errors='ignore') as content_file:
        html = content_file.read()
    html = html.format(**diz_html)
    return html

def render_tabella_ospiti(dati_tabella):
    lista_html = ['<table class="tabella_ospiti table">']
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
        lista_pulsanti.append("""<li class='pulsanti_menu'><a href="{appserver}" class="btn btn-round btn-block pulsanti_menu">Home</a></li>""")
    if diz_html['page'] != 'profilazione':
            lista_pulsanti.append("""<li  class='pulsanti_menu'><a href="{appserver}/profilazione/" class="btn btn-round btn-block pulsanti_menu">Profilazione</a></li>""")
    if diz_html['page'] != 'info':
        lista_pulsanti.append("""<li  class='pulsanti_menu'><a href="{appserver}/info/" class="btn btn-round btn-block pulsanti_menu">Info</a></li>""")
    if diz_html['page'] != 'admin' and diz_html['hash'] == 'super_user':
        lista_pulsanti.append("""<li  class='pulsanti_menu'><a href="{appserver}/admin/" class="btn btn-round btn-block pulsanti_menu">Admin</a></li>""")
    if diz_html['hash'] == 'super_user':
        lista_pulsanti.append("""<li  class='pulsanti_menu'><a href="{appserver}/gallery/" class="btn btn-round btn-block pulsanti_menu">Gallery</a></li>""")
    lista_pulsanti.append("""<li  class='pulsanti_menu'><a onclick="logout()" class="btn btn-round btn-block pulsanti_menu">Logout</a></li>""")

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
    DIR = settings.IMG_DIR + '/%s/' % tipo_carosello
    elenco_file = os.listdir(DIR)
    elenco_file = [i for i in elenco_file if i != '.DS_Store']
    if rand:
        random.shuffle(elenco_file)
    posizione = 'assets/img/%s' % tipo_carosello
    return crea_html_carosello(elenco_file, posizione)


def indicators_carosello(tipo_carosello, id_carosello):
    DIR = settings.IMG_DIR + '/%s/' % tipo_carosello
    elenco_file = os.listdir(DIR)
    elenco_file = [i for i in elenco_file if i != '.DS_Store']
    html = ["""<li data-target="#%s" data-slide-to="0" class="active"></li>""" % id_carosello]
    for index in range(1, len(elenco_file)):
        html.append("""<li data-target="#{id_carosello}" data-slide-to="{index}"></li>""".format(**locals()))
    return ''.join(html)


def crea_html_carosello(lista_file, posizione):
    html = []
    count = 0
    flag_selected = False
    for name in lista_file:
        count += 1
        if name == 'foto1.jpeg':
            selected = 'active'
            flag_selected = True
        else:
            selected = ''
            if not flag_selected and count == len(lista_file):
                selected = 'active'

        html.append("""
           <div class="item {selected}">
               <img src="{posizione}/{name}" alt="{name}">
           </div>
           """.format(**locals()))
    return ''.join(html)


def get_elenco_file_gallery():
    DIR = settings.IMG_DIR + 'gallery/original/'

    html = []
    elenco_file = os.listdir(DIR)
    elenco_file.sort(key=lambda x: os.stat(os.path.join(DIR, x)).st_mtime, reverse=True)
    elenco_file = [i for i in elenco_file if i != '.DS_Store']
    step = 4
    for i in range(0, len(elenco_file), step):
        html.append("""
        <div class="row">
        """)
        for k in range(i, min(i+step, len(elenco_file))):
            img = elenco_file[k]
            d_format = {
                'url': '../assets/img/gallery/miniature/' + img,
                'img': img
            }
            html.append("""
                <div class="col-sm-3">
                    <img src="{url}" class="img-thumbnail"> <i class="fas fa-download fa-2x"></i>
                </div>
            """.format(**d_format))

        html.append("""
           </div>
           """)

    html = ''.join(html)
    return html