from django.db import models
import hashlib


class Ospite(models.Model):

    choices = [
        ('S','on'),
        ('N','off'),
    ]

    id_ospite = models.AutoField(max_length=11, primary_key=True)
    nome = models.Field(name='nome', blank=True)
    speciale = models.CharField(max_length=1, choices=choices, default='N')
    albergo = models.CharField(max_length=1, choices=choices, default='N')
    mail = models.CharField(max_length=100, blank=True)
    viaggio = models.CharField(max_length=1, choices=choices, default='N')
    note = models.Field(blank=True)
    url_img_user = models.Field(blank=True, default='assets/img/mockup.png')
    menu = models.Field(blank=True, default='bambino')
    utente = models.Field(blank=True)

    class Meta:
        db_table = 'ospiti'
        app_label = 'matrimonio'

    def toHtml(self):
        check_fields = ['albergo', 'viaggio']
        for item in check_fields:
            value = self.__getattribute__(item)
            self.__setattr__(item, '' if value == 'N' else 'checked')

        self.select_bambino = ''
        self.select_carne = ''
        self.select_pesce = ''
        self.select_carne_senza_glutine = ''
        self.select_pesce_senza_glutine = ''
        self.select_carne_senza_lattosio = ''
        self.select_pesce_senza_lattosio = ''

        self.__setattr__('select_%s' % self.menu, 'selected')

        return self.__dict__


class Famiglia(models.Model):
    id_famiglia = models.AutoField(max_length=11, primary_key=True)
    alias = models.Field(name='alias', blank=True)
    hash = models.Field(name='hash', blank=True)

    class Meta:
        db_table = 'famiglie'
        app_label = 'matrimonio'

    def calcola_hash(self):
        self.hash = hashlib.md5(self.alias.encode('utf-8')).hexdigest()[:10]
        self.save()