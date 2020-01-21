from matrimonio import settings

from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import pagesizes, units, utils
import qrcode


def genera_partecipazione(alias, hash):
    path_file = '%s/%s.pdf' % (settings.DOCDIR, alias)
    c = canvas.Canvas(path_file, pagesize=pagesizes.landscape(pagesizes.A5))
    c.setFontSize(12)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(settings.APPSERVER + '/fast_login/?hash=' + hash)
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white")

    img_jpeg = img.convert('RGB')
    img_jpeg.save(settings.DOCDIR + '/qr.jpeg')
    img_for_print = utils.ImageReader(settings.DOCDIR + '/qr.jpeg')

    c.drawImage(img_for_print, units.cm * 8, units.cm * 5, width=units.cm * 5, height=units.cm * 5)
    testo = settings.APPSERVER + '/fast_login/?hash=' + hash
    c.drawString(units.cm * 4, units.cm * 4, testo)
    testo = 'Ciao, inquadra il QR code oppure vai su %s e digita il codice: %s' % (settings.APPSERVER, hash)
    c.drawString(units.cm * 2, units.cm * 3, testo)
    c.save()

def genera_segnaposto(lista_ospiti):
    path_file = '%s/segnaposto.pdf' % (settings.DOCDIR)
    c = canvas.Canvas(path_file, pagesize=pagesizes.A3)

    righe = 0
    for riga in range(0,len(lista_ospiti), 4):
        righe += 1
        colonna = 0
        for cella in range(riga, min(riga+4, len(lista_ospiti))):
            c.drawString(units.cm * colonna * 10 + units.cm, units.cm * riga + units.cm, lista_ospiti[cella].upper())
            colonna += 1

    c.save()

    pass