from matrimonio import settings
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes, units, utils, colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('mvboli', settings.FONT_DIR+'mvboli.ttf'))
pdfmetrics.registerFont(TTFont('papyrus', settings.FONT_DIR+'papyrus.ttf'))

import qrcode

def genera_partecipazione(dict_famiglia):
    url = settings.APPSERVER
    url = 'https://www.marcoemarialaura.com'
    path_file = '%s/partecipazione/part_%s.pdf' % (settings.DOCDIR, dict_famiglia['alias'])
    c = canvas.Canvas(path_file, pagesize=pagesizes.portrait(pagesizes.A7))
    c.setFontSize(6)

    testo = '[fam. {alias}]'.format(**dict_famiglia)
    c.drawString(units.cm * 3, units.cm * 12, testo)



    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(url + '/fl/?hash=' + dict_famiglia['hash'])
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white")
    img_jpeg = img.convert('RGB')
    img_jpeg.save(settings.DOCDIR + '/qr.jpeg')
    img_for_print = utils.ImageReader(settings.DOCDIR + '/qr.jpeg')

    c.drawImage(img_for_print, x=units.cm * 2.4, y=units.cm * 5.5, width=units.cm * 3, height=units.cm * 3)
    testo = url + '/fl/?hash=' + dict_famiglia['hash']
    c.drawString(units.cm * 1, units.cm * 5, testo)
    c.setFontSize(8)
    testo = 'Inquadra il QR code oppure vai su:'
    c.drawString(units.cm * 1.5, units.cm * 3.7, testo)
    testo = '%s' % (url)
    c.drawString(units.cm * 1.5, units.cm * 3, testo)
    testo = 'Per accedere usa il codice: {hash} '.format(**dict_famiglia)
    c.drawString(units.cm * 1, units.cm * 2.3, testo)

    c.save()


def genera_segnaposto(nome):
    path_file = '%s/segnaposto/%s.pdf' % (settings.DOCDIR, nome)
    dimensione = (9 * units.cm, 1.8 * units.cm)
    c = canvas.Canvas(path_file, pagesize=dimensione)

    c.setFont('mvboli', 0.6*units.cm)
    c.drawCentredString(4.5*units.cm, 0.6*units.cm, nome.upper())
    c.save()


def genera_copertina(citazione):
    sfondo = settings.IMG_DIR + 'coperchio_bomboniera2.jpg'

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
            par_nero("<i></i>".format(**citazione), font=15, align=TA_RIGHT, lead= 15)
        ],
        [
            par_nero("<i>{canzone}</i>".format(**citazione), font=15, align=TA_RIGHT, lead= 15)
        ],
        [
            par_nero("{autore}".format(**citazione), font=15, align=TA_RIGHT, lead= 15)
        ],

    ]

    style_row = TableStyle([])
    #style_row.add('LINEABOVE', (0, 0), (-1, 0), 0.25, colors.grey)
    #style_row.add('LINEBELOW', (0, 0), (-1, 0), 0.25, colors.grey)
    #style_row.add('LINEAFTER', (-1, 0), (-1, 0), 0.25, colors.grey)
    #style_row.add('LINEBEFORE', (0, 0), (0, 0), 0.25, colors.grey)

    table = Table(tabella_testo, colWidths=11.5*units.cm, style=style_row)
    table.wrapOn(c, citazione['margin_left']*units.cm, citazione['margin_bottom']*units.cm)
    table.drawOn(c, citazione['margin_left']*units.cm, citazione['margin_bottom']*units.cm)

    c.save()


def genera_lettera(citazione):

    path_file = '%s/lettere/lett_%s%s.pdf' % (settings.DOCDIR, citazione['id_frase'], citazione['canzone'])

    row = len(citazione['testo'].split('''
'''))
    print(citazione['canzone'])

    size = 6 if row <80 else 4

    size = 0
    if row < 35:
        size = 10
    elif row < 55:
        size = 8
    elif row < 60:
        size = 6
    else:
        size = 4

    size = int(6 + (100/row))
    size = size if row < 80 else 6
    size = 10 if row < 38 else size



    #citazione['autore'] = ' righe %s %%s' % row % size

    tabella_testo = [
        [
            par_nero("""{canzone}<br/><br/>""".format(**citazione), font=12, align=TA_CENTER, fontName='papyrus')

        ],
        [
            #par_nero("{testo}".format(**citazione), font=size, lead=size, align=TA_CENTER, fontName='Times-BoldItalic')
            par_nero("{testo}".format(**citazione), font=size, lead=size, align=TA_CENTER, fontName='papyrus')
        ],
        [
            #par_nero("{autore}".format(**citazione), font=8, align=TA_RIGHT)
            par_nero("{autore}".format(**citazione), font=8, align=TA_RIGHT, fontName='papyrus')
        ]
    ]

    style_row = TableStyle([])
    #style_row.add('LINEABOVE', (0, 0), (-1, -1), 0.25, colors.grey)
    #style_row.add('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.grey)
    #style_row.add('LINEAFTER', (0, 0), (-1, -1), 0.25, colors.grey)
    #style_row.add('LINEBEFORE', (0, 0), (-1, -1), 0.25, colors.grey)
    table = Table(tabella_testo, colWidths=12 * units.cm, style=style_row)


    doc = SimpleDocTemplate(path_file, pagesize=(13*units.cm, 21*units.cm))
    margin_top = 0.5 if row > 60 else (90/row)
    doc.topMargin = units.cm * margin_top
    doc.bottomMargin = 0.5 *units.cm

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