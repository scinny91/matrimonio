# -*- coding: utf-8 -*-
from email.message import EmailMessage
import smtplib
import os
import time
from datetime import datetime
import operator

from matrimonio.backand.bo import base, doc
from matrimonio import settings

testo = """
Benvenuto {nome},
Siamo lieti di averti ospite nel giorno più bello della nostra vita.

Ti ringraziamo per esserti profilato e permetterci così di poter organizzare il nostro evento al meglio.
Non perdere il codice "{utente}" fornito nella partecipazione oppure il nome inserito in fase di profilazione ({nome}) per poter accedere nuovamente al sito.

#stayTuned
Marco&Marialaura


{url}
"""


def main(args):
    pulisci_immagini()
    crea_hash()
    invia_mail_aggiornamento()
    crea_segnaposto()
    invia_mail_covid()

def crea_hash():
    #print('creo hash famiglie')
    elenco_famiglie = base.Famiglia.objects.filter()
    for famiglia in elenco_famiglie:
        if not famiglia.hash:
            famiglia.calcola_hash()
        famiglia.genera_partecipazione()

def crea_segnaposto():
    print('creo segnaposto')
    elenco_ospiti = base.Ospite.objects.filter()
    elenco_ospiti = sorted(elenco_ospiti, key=operator.attrgetter('tavolo.nome'))
    lista_nomi = []
    for ospite in elenco_ospiti:
        if ospite.nome:
            if ospite.flag_stampato_segnaposto == 'N':
                doc.genera_segnaposto(ospite.nome)
                ospite.flag_stampato_segnaposto = 'S'
                ospite.save()
            uuid = ospite.nome
            lista_nomi.append((uuid.split(' ')[0], ospite.tavolo.nome))
    doc.genera_segnaposto_bottiglia(lista_nomi)

def invia_mail_aggiornamento():
    print('invia_mail_aggiornamento')
    elenco_ospiti = base.Ospite.objects.filter(
                mail_valida='N'
            ).exclude(mail='')

    for ospite in elenco_ospiti:
        ospite.url = settings.APPSERVER + '/fast_login/?hash=' + ospite.utente
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        msg = EmailMessage()
        msg.set_content(testo.format(**ospite.__dict__))

        msg['Subject'] = 'Benvenuto'
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = ospite.mail
        server.send_message(msg)


        ospite.mail_valida = 'S'
        ospite.save()

    elenco_ospiti = base.Ospite.objects.filter(
                nome='',
            )

    for ospite in elenco_ospiti:
        #gli devo dare a datetime lo stesso timezone che ho sul DB
        ttl = (datetime.now(ospite.upd_ts.tzinfo) - ospite.upd_ts).seconds
        ttl = ttl/3600
        utente = ospite.utente
        if ttl>1:
            print('ospite (famiglia {utente} senza nome da {ttl} ore, lo cavo!'.format(**locals()))
            ospite.delete()
        else:
            print('ospite (famiglia {utente} senza nome da {ttl} ore, aspetto a cancellarlo cavo!'.format(**locals()))

def pulisci_immagini():
    elenco_immagini_ospiti = []
    for o in base.Ospite.objects.filter():
        name = o.url_img_user
        elenco_immagini_ospiti.append(name.split('/').pop())

    elenco_immagini_system = os.listdir(settings.IMAGE_USER_PATH)

    for file in elenco_immagini_system:
        if os.path.isdir(settings.IMAGE_USER_PATH + file):
            # skip directories
            print('skip %s' % file)
            continue
        if file not in elenco_immagini_ospiti:
            print('rm %s%s' % (settings.IMAGE_USER_PATH, file))
            print('rm %soriginal/%s' % (settings.IMAGE_USER_PATH, file))
            os.remove('%s%s' % (settings.IMAGE_USER_PATH, file))
            try:
                os.remove('%soriginal/%s' % (settings.IMAGE_USER_PATH, file))
            except:
                pass

def invia_mail_covid():
    print('invio mail covid')
    testo = """
Ciao {nome},
Purtroppo il Covid-19 ci impone di adeguare i nostri comportamenti anche nel giorno più bello della nostra vita.

Per chiarezza ricapitoliamo le poche e semplici regole che il protocollo ci impone:
    -Per accedere all'evento in villa sarà obbligatorio presentare l'autocertificazione in allegato a questa mail.
    -Potrà essere rilevata la temperatura corporea, impedendo l'accesso in caso di temperatura >37,5 °C.
    -Resta obbligatorio l'uso della mascherina in tutti i locali chiusi e all'aperto nei casi in cui non è possibile mantenere le distanze di sicurezza.
    -I bambini sotto i 6 anni non sono soggetti ad autocertificazione.

Per evitare assembramenti e velocizzare le operazioni burocratiche legate all'autocertificazione suggeriamo di arrivare con il documento precedentemente compilato.

#stayTuned
Marco&Marialaura


    {url}
    """
    elenco_ospiti = base.Ospite.objects.filter(
        mail_valida='S', mail_covid='N'
    ).exclude(mail='')
    with open(settings.STATIC_HTML + '/AUTOCERTIFICAZIONE GREEN PASS.pdf', 'rb') as content_file:
        content = content_file.read()
    for ospite in elenco_ospiti:
        ospite.url = settings.APPSERVER + '/fast_login/?hash=' + ospite.utente
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        msg = EmailMessage()
        msg.set_content(testo.format(**ospite.__dict__))
        msg.add_attachment(content, maintype='application', subtype='pdf', filename='example.pdf')
   
        msg['Subject'] = 'Matrimomoio - GREEN PASS'
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = ospite.mail
        server.send_message(msg)

        ospite.mail_covid = 'S'
        ospite.save()