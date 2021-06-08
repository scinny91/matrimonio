# -*- coding: utf-8 -*-
from email.message import EmailMessage
import smtplib
import os
import time
from datetime import datetime

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

def crea_hash():
    print('creo hash famiglie')
    elenco_famiglie = base.Famiglia.objects.filter()
    for famiglia in elenco_famiglie:
        if not famiglia.hash:
            famiglia.calcola_hash()
        famiglia.genera_partecipazione()

def crea_segnaposto():
    print('creo segnaposto')
    elenco_ospiti = base.Ospite.objects.filter()
    print(elenco_ospiti)
    doc.genera_segnaposto([i.nome for i in elenco_ospiti])
    doc.genera_copertina()

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
        ttl = (datetime.now(ospite.upd_ts.tzinfo) - ospite.upd_ts).days
        if ttl:
            utente = ospite.utente
            print('ospite (famiglia {utente} senza nome da {ttl} giorni, lo cavo!'.format(**locals()))
            ospite.delete()

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