# -*- coding: utf-8 -*-
from email.message import EmailMessage
import smtplib
import os

from matrimonio.backand.bo import base, doc
from matrimonio import settings

testo = """
benvenuto {nome},
Siamo lieti di averti ospite nel giorno più bello della nostra vita.

Innanzitutto ti ringraziamo per l'esserti profilato e permetterci così di poter organizzare il nostro evento al meglio.

#stayTuned
Marco&Marialaura
"""


def main(args):
    pulisci_immagini()
    crea_hash()
    #invia_mail_aggiornamento()

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
            )
    for ospite in elenco_ospiti:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        msg = EmailMessage()
        msg.set_content(testo.format(**ospite.__dict__))

        msg['Subject'] = 'Benvenuto'
        msg['From'] = 'mscinic@gmail.com'
        msg['To'] = ospite.mail
        server.send_message(msg)


        ospite.mail_valida = 'S'
        ospite.save()


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