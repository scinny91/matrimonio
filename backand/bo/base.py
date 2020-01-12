from django.db import models
from matrimonio import settings

import hashlib
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes, units, utils
import qrcode

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

    def genera_partecipazione(self):
        print('genero %s' % self.alias)
        path_file = '%s/%s.pdf' % (settings.DOCDIR, self.alias)
        c = canvas.Canvas(path_file, pagesize=pagesizes.landscape(pagesizes.A5))

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr.add_data(settings.APPSERVER + '/fast_login?hash=' + self.hash)
        qr.make()
        img = qr.make_image(fill_color="black", back_color="white")

        img_jpeg = img.convert('RGB')
        img_jpeg.save(settings.DOCDIR + '/qr.jpeg')
        img_for_print = utils.ImageReader(settings.DOCDIR + '/qr.jpeg')

        c.drawImage(img_for_print, units.cm*8, units.cm*5, width=units.cm*5, height=units.cm*5)

        testo = 'Ciao, inquadra il QR code oppure vai su %s e digita il codice: %s' % (settings.APPSERVER, self.hash)
        c.drawString(units.cm*2, units.cm*3, testo)

        c.save()