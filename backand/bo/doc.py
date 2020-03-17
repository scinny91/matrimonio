from matrimonio import settings
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes, units, utils, colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('mvboli', 'matrimonio/html/mvboli.ttf'))

import qrcode

def genera_partecipazione(alias, hash):
    path_file = '%s/partecipazione/part_%s.pdf' % (settings.DOCDIR, alias)
    c = canvas.Canvas(path_file, pagesize=pagesizes.landscape(pagesizes.A5))
    c.setFontSize(10)
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
    c.drawString(units.cm * 1, units.cm * 3, testo)
    c.save()


def genera_segnaposto(nome):
    path_file = '%s/segnaposto/%s.pdf' % (settings.DOCDIR, nome)
    dimensione = (9 * units.cm, 1.8 * units.cm)
    c = canvas.Canvas(path_file, pagesize=dimensione)
    #c.setFontSize(0.6*units.cm)
    c.setFont('mvboli', 0.6*units.cm)
    c.drawCentredString(4.5*units.cm, 0.6*units.cm, nome.upper())
    c.save()


def genera_copertina(citazione):
    sfondo = 'matrimonio/html/assets/img/coperchio_bomboniera.jpg'

    img_for_print = utils.ImageReader(sfondo)
    print(citazione['canzone'])
    path_file = '%s/copertine/cop_%s%s.pdf' % (settings.DOCDIR, citazione['id_frase'], citazione['canzone'])

    dimensione = (19*units.cm, 27*units.cm)
    c = canvas.Canvas(path_file, pagesize=dimensione)
    c.setFontSize(10)
    c.drawImage(img_for_print, 0, 10, dimensione[0], dimensione[1])


    tabella_testo = [
        [
            par_nero('...{citazione}...'.format(**citazione), font=citazione['font'], lead=citazione['lead'], fontName='mvboli', align=TA_CENTER)
        ],
        [
            par_nero("<i>{canzone}</i>".format(**citazione), font=15, align=TA_RIGHT)
        ],
        [
            par_nero("{autore}".format(**citazione), font=15, align=TA_RIGHT)
        ],
        [
            par_nero("{font}, {lead}".format(**citazione), font=15, align=TA_RIGHT)
        ]
    ]

    style_row = TableStyle([])
    style_row.add('LINEABOVE', (0, 0), (-1, 0), 0.25, colors.grey)
    style_row.add('LINEBELOW', (0, 0), (-1, 0), 0.25, colors.grey)
    style_row.add('LINEAFTER', (-1, 0), (-1, 0), 0.25, colors.grey)
    style_row.add('LINEBEFORE', (0, 0), (0, 0), 0.25, colors.grey)

    table = Table(tabella_testo, colWidths=11.5*units.cm, style=style_row)
    table.wrapOn(c, citazione['margin_left']*units.cm, citazione['margin_bottom']*units.cm)
    table.drawOn(c, citazione['margin_left']*units.cm, citazione['margin_bottom']*units.cm)

    c.save()


def genera_lettera(citazione):

    path_file = '%s/lettere/lett_%s%s.pdf' % (settings.DOCDIR, citazione['id_frase'], citazione['canzone'])

    row = len(citazione['testo'].split('''
'''))
    print(citazione['canzone'])
    print(row)

    size = 6 if row <80 else 4

    tabella_testo = [
        [
            par_nero("{canzone}".format(**citazione), font=8, align=TA_CENTER)

        ],
        [
            par_nero("{testo}".format(**citazione), font=size, lead=size, align=TA_CENTER, fontName='Times-BoldItalic')
        ],
        [
            par_nero("{autore}".format(**citazione), font=8, align=TA_RIGHT)
        ]
    ]

    style_row = TableStyle([])
    style_row.add('LINEABOVE', (0, 0), (-1, -1), 0.25, colors.grey)
    style_row.add('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.grey)
    style_row.add('LINEAFTER', (0, 0), (-1, -1), 0.25, colors.grey)
    style_row.add('LINEBEFORE', (0, 0), (-1, -1), 0.25, colors.grey)
    table = Table(tabella_testo, colWidths=8 * units.cm, style=style_row)


    doc = SimpleDocTemplate(path_file, pagesize=(12*units.cm, 20*units.cm))
    doc.topMargin = 1* units.cm
    doc.build([table])


def par_nero(l, font=6, align=TA_CENTER, fontName='Helvetica', color='black', lead=6, indent=2):
    par_style = ParagraphStyle('Normal')
    par_style.fontName = fontName

    par_style.fontSize = font
    par_style.alignment = align
    par_style.textColor = eval('colors.%s' % color)
    if align == TA_RIGHT:
        par_style.rightIndent = indent
    elif align == TA_LEFT:
        par_style.leftIndent = indent
    par_style.leading = lead
    par_style.space_before = 0
    par_style.space_after = 0
    par_style.borderPadding = 0
    par_style.splitLongWords = 0

    par_style.wordWrap = 'LTR'  # per andare a capo quando ci sonoi <BR/>
    if type(l) == type([]) or type(l) == type(()):
        data = []
        for item in l:
            if '\n' in item:
                lista_sotto_items = item.split('\n')
                for si in lista_sotto_items:
                    data.append(Paragraph(si, par_style))
            else:
                data.append(Paragraph(item, par_style))
        return data
    else:
        if '\n' in l:
            data = []
            for riga in l.split('\n'):
                data.append(Paragraph(riga, par_style))
            return data
        else:
            p = Paragraph(l, par_style)
            return p