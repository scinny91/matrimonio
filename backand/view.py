import pprint
import random
import codecs
import os
from datetime import datetime, timezone

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


def render_guestbook(diz_html):
    with codecs.open(settings.STATIC_HTML + '/html/guestbook.html', 'r', encoding='utf-8', errors='ignore') as content_file:
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
    invitato['mostra_albergo'] = ''
    if famiglia.albergo_abilitato != 'S':
        invitato['mostra_albergo'] = 'nascosta'
    return render_blocco_righe_invitato(invitato)


def render_menu(diz_html):
    lista_pulsanti = []

    tap_selezionato = ''
    if diz_html['page'] == 'index':
        tap_selezionato = 'menu_selected'
    lista_pulsanti.append("""<li><a href="{appserver}" class="btn btn-round btn-block pulsanti_menu %s">Home</a></li>""" % tap_selezionato)

    tap_selezionato = ''
    if diz_html['page'] == 'profilazione':
        tap_selezionato = 'menu_selected'
    lista_pulsanti.append("""<li><a href="{appserver}/profilazione/" class="btn btn-round btn-block pulsanti_menu %s">Profilazione</a></li>""" % tap_selezionato)

    tap_selezionato = ''
    if diz_html['page'] == 'info':
        tap_selezionato = 'menu_selected'
    lista_pulsanti.append("""<li><a href="{appserver}/info/" class="btn btn-round btn-block pulsanti_menu %s">Info</a></li>""" % tap_selezionato)

    tap_selezionato = ''
    if diz_html['page'] == 'viaggio':
        tap_selezionato = 'menu_selected'
    lista_pulsanti.append("""<li><a href="{appserver}/viaggio/" class="btn btn-round btn-block pulsanti_menu %s">Viaggio di nozze</a></li>""" % tap_selezionato)

    tap_selezionato = ''
    if diz_html['page'] == 'guestbook':
        tap_selezionato = 'menu_selected'
    lista_pulsanti.append("""<li><a href="{appserver}/guestbook/" class="btn btn-round btn-block pulsanti_menu %s">Guestbook</a></li>""" % tap_selezionato)

    if diz_html['hash'] == 'super_user':
        tap_selezionato = ''
        if diz_html['page'] == 'admin':
            tap_selezionato = 'menu_selected'
        lista_pulsanti.append("""<li><a href="{appserver}/admin/" class="btn btn-round btn-block pulsanti_menu %s">Admin</a></li>""" % tap_selezionato)

    if diz_html['hash'] == 'super_user':
        tap_selezionato = ''
        if diz_html['page'] == 'gallery':
            tap_selezionato = 'menu_selected'
        lista_pulsanti.append("""<li ><a href="{appserver}/gallery/" class="btn btn-round btn-block pulsanti_menu %s">Gallery</a></li>""" % tap_selezionato)

    lista_pulsanti.append("""<li><a onclick="logout()" class="btn btn-round btn-block pulsanti_menu">Logout</a></li>""")

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


def render_blocco_righe_invitato(diz_invitato):
    return """
        <div class="row riga_invitato" id="riga_invitato_{id_ospite}">

                <div class="col-sm-3">
                        <img src="../{url_img_user}" alt="Circle Image" class="img-circle" id='img_{id_ospite}'>

                </div>
                <div class="col-md-9">
                    <div class="row">
                        <div class="col-sm-3 lbl">
                            <input type="file" class="form-control-file" id="foto_{id_ospite}" onchange='uploadFile(this)' name="foto_{id_ospite}" style="display: none;" >
                            <label for="foto_{id_ospite}" >
                                <span> <i class="fas fa-upload fa-2x"></i> Carica la foto!</span>
                            </label>
                        </div>
                        <div class="col-sm-3 lbl">
                           <div class='delete_ospite'  id='cancella_ospite_{id_ospite}'>
                               <label>
                                    <span> <i class="fas fa-user-times fa-2x"></i>  Elimina ospite!</span>
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-sm-4 lbl">
                            <div class="input-group">
                                <span class="input-group-addon">Nome:</span>
                                <input type="text" value="{nome}" name='nome' placeholder="Digita il nome dell'ospite" class="form-control onchangeupdate" id='nome_ospite_{id_ospite}' />
                            </div>
                        </div>
                        <div class="col-sm-4 lbl">
                            <div class="input-group">
                                <span class="input-group-addon">Mail:</span>
                                <input type="text" value="{mail}" name='mail' placeholder="Inserisci un indirizzo mail" class="form-control onchangeupdate" id='mail_{id_ospite}' />
                            </div>
                        </div>
                        <div class="col-sm-4 lbl">
                            <div class="input-group">
                                <span class="input-group-addon">Sesso:</span>
                                <select class="form-control onchangeupdate" id="sesso_{id_ospite}" name='sesso'>
                                      <option {select_uomo} value='Uomo'>Uomo</option>
                                      <option {select_donna} value='Donna'>Donna</option>
                                </select> 
                            </div>
                        </div>

                    </div>
                    <div class="row">
                        <div class="col-sm-4 lbl">
                            <div class="input-group">
                                <span class="input-group-addon">Note:</span>
                                 <textarea class="form-control onchangeupdate" id="note_{id_ospite}" rows="2" name='note'></textarea>
                            </div>
                        </div>
                        <div class="col-sm-4 lbl">
                            <div class="input-group">
                                <span class="input-group-addon">Menu:</span>
                                <select class="form-control onchangeupdate" id="menu_{id_ospite}" name='menu'>
                                      <option {select_bambino} value='bambino'>Bambino</option>
                                      <option {select_adulto} value='adulto'>Carne</option>
                                      <option {select_senza_glutine} value='senza_glutine'>Senza glutine</option>
                                      <option {select_senza_lattosio} value='senza_lattosio'>Senza lattosio</option>
                                </select>
                            </div>
                        </div>

                        <div class="col-sm-4 lbl">
                            <div class="input-group {mostra_albergo}">
                               <span class="input-group-addon">Albergo:</span>
                                <div class="input-group-addon">
                                    <div class="switch-unload" id='switchAlbergo_{id_ospite}'  
                                    data-on-label="<i class='fa fa-check'></i>" 
                                    data-off-label="<i class='fa fa-times'></i>">
                                      <input type="checkbox" {albergo} id='albergo_{id_ospite}' class='onchangeupdate'  name='albergo'/>
                                </div>
                                 </div>

                            </div>
                        </div>




                    </div>
                </div>
        </div>
    """.format(**diz_invitato)


def render_tabella_commenti(commenti, dati_utente):
    html = []

    for commento in commenti:


        if commento['info_ospite']:
            commento['immagine_utente'] = """ <img src="../{url_img_user}" alt="foto {nome}" class="img-circle " width=120px>""".format(**commento['info_ospite'])
        else:
            commento['immagine_utente'] = """ <img src="../assets/img/mockup.png" alt="foto utente cancellato" class="img-circle " width=120px>"""


        commento['rif_ospite'] = '<b>Utente cancellato</b>'
        if commento['info_ospite']:
            commento['rif_ospite'] = '<b>%s</b> - Famiglia: %s' % (commento['info_ospite']['nome'], commento['info_famiglia']['nome_famiglia'])






        ora_commento = commento['ins_ts'].strftime('%Y-%m-%d %H:%M:%S')
        delta_days = datetime.now() - datetime.strptime(ora_commento, '%Y-%m-%d %H:%M:%S')

        minuti = int(delta_days.seconds / 60)
        ore = int(minuti / 60)
        giorni = int(ore / 24)
        mesi = int(giorni / 30)
        anni = int(mesi / 12)

        if anni:
            commento['delta_time'] = 'Scritto: %s anni fa' % anni
        elif mesi:
            commento['delta_time'] = 'Scritto: %s mesi fa' % mesi
        elif giorni:
            commento['delta_time'] = 'Scritto: %s giorni fa' % giorni
        elif ore:
            commento['delta_time'] = 'Scritto: %s ore fa' % ore
        elif minuti:
            commento['delta_time'] = 'Scritto: %s minuti fa' % minuti
        else:
            commento['delta_time'] = 'Scritto: adesso'


        html.append("""
        <div class="row tim-row">
            <div class="col-sm-2"></div>
            <div class="col-sm-2">{immagine_utente}</div>
            <div class="col-sm-6">
                <div class='messaggio'>
                {rif_ospite}
                <br>
                {descrizione}
                </div>
                <div class='messaggio messaggio-small'>
                    <small class="opacity-65">{delta_time}</small>
                </div>
                
            </div>
            <div class="col-sm-2"></div>
        </div>
        """.format(**commento))

    if not html:
        html.append('''
        <div class="row" style="margin-top: 100px">
            <div class="col-sm-2"></div>
            <div class="col-sm-6">Nessun commento presente</div>
            <div class="col-sm-2"></div>
        ''')
    if dati_utente:
        opz_utente = []
        for utente in dati_utente:
            opz_utente.append("""
                <option value='{nome}'>{nome}</option>
            """.format(**utente.__dict__))
        opz_utente = ''.join(opz_utente)

        html.append("""
        <div class="row tim-row">
            <div class="col-sm-2 "> </div>
            <div class="col-sm-2 ">
                Utente che commenta: <br>
                
            </div>
            <div class="col-sm-3">
                <select name='utente_commento'>
                  {0}
                </select> 
            </div>
            <div class="col-sm-3"><button class="btn btn-block btn-l btn-info btn-square add_comment">Commenta</button></div>
            <div class="col-sm-2"></div>
        </div>
        <div class="row">
            <div class="col-sm-2 "> </div>
            <div class="col-sm-8">
                Commento:<br>
                <textarea class="form-control" rows="10" name='nuovo_commento' id='commento'></textarea>
                
            </div>
            <div class="col-sm-2"></div>
        </div>
        """.format(opz_utente))
    else:
        html.append("""
                <div class="row tim-row">
                    <div class="col-sm-2 "> </div>
                    <div class="col-sm-8 "><b>Prima di poter aggiungere un commento è necessario registrare almeno un ospite nella sezione PROFILAZIONE.</b></div>
                    <div class="col-sm-2 "> </div>
                </div>
                """)


    return ''.join(html)