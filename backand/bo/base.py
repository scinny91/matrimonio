from django.db import models
from matrimonio.backand.bo import doc
import hashlib
from datetime import datetime

class Ospite(models.Model):

    choices = [
        ('S','on'),
        ('N','off'),
    ]

    id_ospite = models.AutoField(max_length=11, primary_key=True)
    nome = models.Field(name='nome', blank=True)
    speciale = models.CharField(max_length=10, choices=choices, default='')
    albergo = models.CharField(max_length=1, choices=choices, default='N')
    mail = models.CharField(max_length=100, blank=True)
    mail_valida = models.CharField(max_length=100, blank=True, default='N')
    sesso = models.CharField(default='Uomo')
    note = models.Field(blank=True)
    url_img_user = models.Field(blank=True, default='assets/img/mockup.png')
    menu = models.Field(blank=True, default='bambino')
    utente = models.Field(blank=True)
    upd_ts = models.DateTimeField(name='upd_ts', auto_now=True)

    class Meta:
        db_table = 'ospiti'
        app_label = 'matrimonio'

    def toHtml(self, famigliaObj):
        check_fields = ['albergo']
        for item in check_fields:
            value = self.__getattribute__(item)
            self.__setattr__(item, '' if value == 'N' else 'checked')

        self.select_bambino = ''
        self.select_adulto = ''
        self.select_senza_glutine = ''
        self.select_senza_lattosio = ''
        self.__setattr__('select_%s' % self.menu, 'selected')

        self.select_uomo = ''
        self.select_donna = ''
        self.__setattr__('select_%s' % self.sesso, 'selected')

        self.mostra_albergo = ''
        if famigliaObj.albergo_abilitato != 'S':
            self.mostra_albergo = 'nascosta'
        return self.__dict__


class Famiglia(models.Model):
    id_famiglia = models.AutoField(max_length=11, primary_key=True)
    alias = models.Field(name='alias', blank=True)
    hash = models.Field(name='hash', blank=True)
    nome_famiglia = models.Field(name='nome_famiglia', blank=True)
    albergo_abilitato = models.Field(name='albergo_abilitato', blank=True)
    upd_ts = models.DateTimeField(name='upd_ts', auto_now=True)

    class Meta:
        db_table = 'famiglie'
        app_label = 'matrimonio'

    def calcola_hash(self):
        self.hash = hashlib.md5(self.alias.encode('utf-8')).hexdigest()[:10]
        self.save()

    def genera_partecipazione(self):
        doc.genera_partecipazione(self.alias, self.hash)


class Frase(models.Model):
    id_frase = models.AutoField(max_length=11, primary_key=True)
    testo = models.Field(name='testo', blank=True)
    citazione = models.Field(name='citazione', blank=True)
    canzone = models.Field(name='canzone', blank=True)
    autore = models.Field(name='autore', blank=True)
    font = models.Field(name='font', blank=True)
    lead = models.Field(name='lead', blank=True)
    margin_left = models.Field(name='margin_left', blank=True)
    margin_bottom = models.Field(name='margin_bottom', blank=True)
    class Meta:
        db_table = 'frasi'
        app_label = 'matrimonio'


class Commento(models.Model):
    id_commento = models.AutoField(max_length=11, primary_key=True)
    utente_commento = models.Field(name='utente_commento', blank=True)
    famiglia = models.Field(name='famiglia', blank=True)
    descrizione = models.Field(name='descrizione', blank=True)
    ins_ts = models.DateTimeField(name='ins_ts', auto_now=True)
    class Meta:
        db_table = 'commenti'
        app_label = 'matrimonio'

    @staticmethod
    def get_commenti_per_html():
        commenti = []
        for i in Commento.objects.filter():
            info_ospite = Ospite.objects.filter(nome=i.utente_commento, utente=i.famiglia)
            if info_ospite:
                i.info_ospite = info_ospite[0].__dict__
            else:
                i.info_ospite = {}

            info_famiglia = Famiglia.objects.filter(hash=i.famiglia)
            if info_famiglia:
                i.info_famiglia = info_famiglia[0].__dict__
            else:
                i.info_famiglia = {}

            commenti.append(i.__dict__)
        return commenti

class ListaNozze(models.Model):
    id_articolo = models.AutoField(max_length=11, primary_key=True)
    nome = models.Field(name='nome', blank=True)
    descrizione = models.Field(name='descrizione', blank=True)
    immagine = models.Field(name='immagine', blank=True)
    stato = models.Field(name='stato', blank=True)
    ins_ts = models.DateTimeField(name='ins_ts', auto_now=True)
    class Meta:
        db_table = 'lista_nozze'
        app_label = 'matrimonio'