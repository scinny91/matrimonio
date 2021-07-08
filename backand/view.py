import pprint
import random
import codecs
import os
from datetime import datetime, timezone
from operator import attrgetter
import itertools

from .bo import base
from matrimonio import settings


def render_index(diz_html):
    diz_html['menu'] = render_menu(diz_html)
    with codecs.open(settings.STATIC_HTML + '/html/index.html', 'r', encoding='utf-8', errors='ignore') as content_file:
        html = content_file.read()
    html = html.format(**diz_html)
    return html


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

def render_tavoli(diz_html):
    with codecs.open(settings.STATIC_HTML + '/html/tavoli.html', 'r', encoding='utf-8', errors='ignore') as content_file:
        html = content_file.read()
    html = html.format(**diz_html)
    return html

def render_lista_nozze(diz_html):
    with codecs.open(settings.STATIC_HTML + '/html/lista_nozze.html', 'r', encoding='utf-8', errors='ignore') as content_file:
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

def render_sezione_albergo():
    return """
    <div class="row">
             <div class="col-sm-3">
                 <h3>Albergo:</h3>
                 <label class="control-label">Holiday Inn Express Reggio Emilia</label>
                 <label class="control-label">Reception: +39 0522507122</label>
                 <label class="control-label">Via Meuccio Ruini n°7,Reggio Emilia, 42100</label>

             </div>
             <div class="col-sm-9 lbl">
                <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2835.0799518522317!2d10.640245351084486!3d44.717979778996664!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47801c301eed65c7%3A0xf0604fe427499001!2sHoliday%20Inn%20Express%20Reggio%20Emilia!5e0!3m2!1sit!2sit!4v1624459141687!5m2!1sit!2sit" width="800" height="600" style="border:0;" allowfullscreen="" loading="lazy"></iframe>            
                </div>
        </div>"""

def render_tabella_lista_nozze(elenco_lista):
    html = []

    for elemento in elenco_lista:
        html.append('''
        <div class="row" >

            <div class="col-sm-1"></div>
            <div class="col-sm-3">
                <div class=''>
                     <h2>{nome} </h2>
                     <br> {descrizione}
                </div>
            </div> 
            <div class="col-sm-5 testo_centrale">
                <div class="text-center">
                 <img src='../assets/img/lista_nozze/{immagine}' class="img-fluid rounded" style='max-width:350px'>
                    
                </div> 
            </div>
            <div class="col-sm-2 testo_centralissimo">
                <div class='' > 
                    {pulsante_html}
                </div>
            </div>
            <div class="col-sm-1"></div> 
        </div>
            '''.format(**elemento.to_html()))
    return ''.join(html)

def render_tabella_ospiti(dati_tabella, tavoli):
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
                 <td class="cella_ospiti title"> Covid </td>
                 <td class="cella_ospiti title"> Speciale </td>  
                 <td class="cella_ospiti title"> Upd TS </td> 
                 <td class="cella_ospiti title"> Azioni </td> 
                </tr>''')
        for ospite in famiglia['invitati']:
            ospite['flag_mail_check'] = ''
            if ospite['mail']:
                ospite['flag_mail_check'] = '<i class="fas fa-check"></i>' if ospite['mail_valida'] == 'S' else '<i class="fas fa-exclamation-circle"></i>'

            ospite['html_selezione_tavolo'] = """
            <div class="input-group">
                <span class="input-group-addon">tavolo:</span>
                    <select class="form-control onchangeupdate" id="tavolo_{id_ospite}" name='tavolo'>
                          {valori_selezione}
                    </select> 
            </div>"""
            valori = []
            for tavolo in tavoli:
                sel = ""
                if ospite['tavolo_id'] == tavolo['id_tavolo']:
                    sel = 'selected'
                valori.append(" <option {sel} value='{tavolo[id_tavolo]}'>{tavolo[nome]}</option>".format(**locals()))
            ospite['valori_selezione'] = ''.join(valori)
            ospite['html_selezione_tavolo'] = ospite['html_selezione_tavolo'].format(**ospite)

            tabella_ospiti.append('''
                                   <tr id='riga_invitato_{id_ospite}'>
                                    <td class="cella_ospiti"> <img src='../{url_img_user}' class='img-piccola'> </td>
                                    <td class="cella_ospiti"> {nome} </td> 
                                    <td class="cella_ospiti"> {mail} {flag_mail_check}</td> 
                                    <td class="cella_ospiti"> {note} </td> 
                                    <td class="cella_ospiti"> {menu} </td> 
                                    <td class="cella_ospiti"> {sesso} </td> 
                                    <td class="cella_ospiti"> {covid_html} </td>
                                    <td class="cella_ospiti"> {speciale} </td>  
                                    <td class="cella_ospiti"> {upd_ts} </td>  
                                    <td class="cella_ospiti"> 
                                        <div class='delete_ospite'  id='cancella_ospite_{id_ospite}'>
                                           <label>
                                                <span> <i class="fas fa-user-times"></i>  Elimina</span>
                                            </label>
                                       </div> 
                                       {html_selezione_tavolo}
                                    </td> 
                                   </tr>'''.format(**ospite))
            #print(ospite)
        lista_html.append('<tr class="famiglia"> <td colspan=5> <table class="tabella_ospiti"> %s </table> </td> </tr>' % ''.join(tabella_ospiti))
    lista_html.append('</table>')

    return ''.join(lista_html)


def render_tabella_tavoli(ospiti):
    lista_html = []

    grouper = attrgetter('tavolo.nome')
    for tavolo, c in itertools.groupby(sorted(ospiti, key=grouper), key=grouper):
        ospiti_tavolo = list(c)
        sezione = []
        for ospite in sorted(ospiti_tavolo, key=attrgetter('utente')):
            sezione.append("""
            <tr>
                <td><img src="../{url_img_user}" alt="Circle Image" class="img-circle img-piccola" id='img_{id_ospite}'> </td>
                <td>{nome}</td>
                <td>{note}</td>
                <td>Menu: {menu}</td>
                <td>Sesso: {sesso}</td>
                <td>Covid: {covid_html}</td>
            </tr>
            """.format(**ospite.toHtml()))

        html_sezione = ''.join(sezione)
        qta_ospiti = len(ospiti_tavolo)
        qta_bambini = len([i for i in ospiti_tavolo if i.menu=='bambino'])
        lista_html.append('''
        <div class='row'>    
            <div class="col-sm-2 title"> Ospiti: {qta_ospiti} ({qta_bambini}) </div>
            <div class="col-sm-4 title"> Nome: {ospite.tavolo.nome} </div>
            <div class="col-sm-2 title"> Bottiglia: {ospite.tavolo.bottiglia}</div>
            <div class="col-sm-2 title"> Note: {ospite.tavolo.note}</div>
            <div class="col-sm-2 title"> {ospite.tavolo.ins_ts} </div>
        <table>  
            {html_sezione}
        </table>  
        </div>'''.format(**locals()))




    return ''.join(lista_html)


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
    lista_pulsanti.append("""<li><a href="{appserver}/viaggio/" class="btn btn-round btn-block pulsanti_menu %s">Lista di nozze</a></li>""" % tap_selezionato)

    if diz_html['hash'] == 'super_user' or diz_html['delta_days'] < 10:
        tap_selezionato = ''
        if diz_html['page'] == 'guestbook':
            tap_selezionato = 'menu_selected'
        lista_pulsanti.append("""<li><a href="{appserver}/guestbook/" class="btn btn-round btn-block pulsanti_menu %s">Guestbook</a></li>""" % tap_selezionato)

    if diz_html['hash'] == 'super_user':
        tap_selezionato = ''
        if diz_html['page'] == 'admin':
            tap_selezionato = 'menu_selected'
        lista_pulsanti.append("""<li><a href="{appserver}/admin/" class="btn btn-round btn-block pulsanti_menu %s">Admin</a></li>""" % tap_selezionato)
        tap_selezionato = ''
        if diz_html['page'] == 'tavoli':
            tap_selezionato = 'menu_selected'
        lista_pulsanti.append("""<li><a href="{appserver}/tavoli/" class="btn btn-round btn-block pulsanti_menu %s">Tavoli</a></li>""" % tap_selezionato)


    if diz_html['hash'] == 'super_user' or diz_html['delta_days'] < 10:
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


def html_carosello(tipo_carosello, rand=True, limit=0):
    DIR = settings.IMG_DIR + '/%s/' % tipo_carosello
    elenco_file = os.listdir(DIR)
    elenco_file = [i for i in elenco_file if i != '.DS_Store']
    if rand:
        random.shuffle(elenco_file)
    if limit:
        elenco_file = elenco_file[:limit]
    posizione = 'assets/img/%s' % tipo_carosello
    return crea_html_carosello(elenco_file, posizione)


def indicators_carosello(tipo_carosello, id_carosello, limit=0):
    DIR = settings.IMG_DIR + '/%s/' % tipo_carosello
    elenco_file = os.listdir(DIR)
    elenco_file = [i for i in elenco_file if i != '.DS_Store']
    if limit:
        elenco_file = elenco_file[:limit]
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
                        <div class="col-sm-2 lbl">
                           <div>
                               <label>
                                    <span> <div class='salva_ospite'  id='salva_ospite_{id_ospite}'>
                                        <i class="fas fa-user-plus fa-2x"></i>Salva</div> </span>
                                </label>
                            </div>
                        </div>
                        <div class="col-sm-4 lbl">
                           <div class='{mostra_albergo} testo_centrato'>
                               <label>
                                    Per te gli sposi hanno previsto l'albergo, contattali per maggiori info!
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-sm-4 lbl">
                            <div class="input-group">
                                <span class="input-group-addon">Nome e cognome:</span>
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
                                      <option {select_Uomo} value='Uomo'>Uomo</option>
                                      <option {select_Donna} value='Donna'>Donna</option>
                                </select> 
                            </div>
                        </div>

                    </div>
                    <div class="row">
                        <div class="col-sm-4 lbl">
                            <div class="input-group">
                                <span class="input-group-addon">Note:</span>
                                 <textarea class="form-control onchangeupdate" id="note_{id_ospite}" rows="2" name='note'>{note}</textarea>
                            </div>
                        </div>
                        <div class="col-sm-4 lbl">
                            <div class="input-group">
                                <span class="input-group-addon">Menu:</span>
                                <select class="form-control onchangeupdate" id="menu_{id_ospite}" name='menu'>
                                      <option {select_adulto} value='adulto'>Adulto</option>
                                      <option {select_bambino} value='bambino'>Bambino</option>
                                      <option {select_senza_glutine} value='senza_glutine'>Senza glutine</option>
                                      <option {select_senza_lattosio} value='senza_lattosio'>Senza lattosio</option>
                                </select>
                            </div>
                        </div>

                        <div class="col-sm-4 lbl">
                            <div class="input-group">
                               <span class="input-group-addon">Covid/Vaccino:</span>
                                <div class="input-group-addon">
                                    <div class="switch-unload" id='switchCovid_{id_ospite}'  
                                    data-on-label="<i class='fa fa-check'></i>" 
                                    data-off-label="<i class='fa fa-times'></i>">
                                      <input type="checkbox" {covid} id='covid_{id_ospite}' class='onchangeupdate'  name='covid'/>
                                </div>
                                 </div>

                            </div>
                        </div>




                    </div>
                </div>
        </div>
    """.format(**diz_invitato)


def render_tabella_commenti(commenti, famiglia_commento):
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

        commento['pulsante_cancella'] = ''
        if commento['info_famiglia']['hash'] == famiglia_commento.hash or famiglia_commento.hash == 'super_user':
            commento['pulsante_cancella'] = """
            <span id="elimina_commento_{id_commento}" class='elimina_commento' title="Elimina commento">
                <i class="fas fa-trash-alt  fa-2x"></i>
            </span>""".format(**commento)

        minuti = int(delta_days.seconds / 60)
        ore = int(minuti / 60)
        giorni = int(delta_days.days)
        mesi = int(giorni / 30)
        anni = int(mesi / 12)

        if anni:
            commento['delta_time'] = 'Scritto: %s anni fa' % anni
        elif mesi:
            commento['delta_time'] = 'Scritto: %s mesi fa' % mesi
        elif giorni > 0:
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
            <div class="col-sm-2">{immagine_utente} {pulsante_cancella}</div>
            <div class="col-sm-6">
                <div class='messaggio'>
                {rif_ospite}
                <br>
                <span class='messaggio_guestbook'>{descrizione}<span>
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

    return ''.join(html)


def render_nuovo_commento(dati_utente):

    if dati_utente:
        opz_utente = []
        for utente in dati_utente:
            opz_utente.append("""
                <option value='{nome}'>{nome}</option>
            """.format(**utente.__dict__))
        opz_utente = ''.join(opz_utente)

        html = """
        <div class="row tim-row">
            <div class="col-sm-2 "> </div>
            <div class="col-sm-2 ">
                Utente che commenta: <br>

            </div>
            <div class="col-sm-3">
                <select name='utente_commento' id='utente_commento'>
                  {0}
                </select> 
            </div>
            <div class="col-sm-3"><button class="btn btn-block btn-l btn-info btn-square add_comment" id='add_comment'>Commenta</button></div>
            <div class="col-sm-2"></div>
        </div>
        <div class="row">
            <div class="col-sm-2 alert"> </div>
            <div class="col-sm-8 alert alert-success testo_centrale nascosta" id='messaggio_successo'>
                Commento inserito con successo
            </div>
            <div class="col-sm-2 "> </div>
        </div>
        <div class="row">
            <div class="col-sm-2 "> </div>
            <div class="col-sm-8">
                Commento:<br>
                <textarea class="form-control" rows="10" name='nuovo_commento' id='commento'></textarea>

            </div>
            <div class="col-sm-2"></div>
        </div>
        """.format(opz_utente)
    else:
        html = """
                <div class="row tim-row">
                    <div class="col-sm-2 "> </div>
                    <div class="col-sm-8 "><b>Prima di poter aggiungere un commento è necessario registrare almeno un ospite nella sezione PROFILAZIONE.</b></div>
                    <div class="col-sm-2 "> </div>
                </div>
                """

    return html