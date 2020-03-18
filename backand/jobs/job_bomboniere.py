from matrimonio.backand.bo import doc, base
from matrimonio import settings
import os, shutil




def main(args):
    if settings.AMBIENTE == 'LOCALE':
        print('Copertine....')
        crea_copertina(args)
        print('Lettere....')
        crea_lettera(args)
    print('Segnposto....')
    crea_segnaposto()

def crea_segnaposto():
    svuota_cartelle('%s/segnaposto' % (settings.DOCDIR))
    elenco_ospiti = base.Ospite.objects.filter()
    for ospite in elenco_ospiti:
        if ospite.nome:
            doc.genera_segnaposto(ospite.nome)


def crea_copertina(args):
    lista_canzoni = base.Frase.objects.filter()
    if args.get('id'):
        print('faccio {id}'.format(**args))
        lista_canzoni = [i for i in lista_canzoni if i.id_frase == int(args['id'])]
    else:
        svuota_cartelle('%s/copertine' % (settings.DOCDIR))
    for brano in lista_canzoni:
        doc.genera_copertina(brano.__dict__)


def crea_lettera(args):
    lista_canzoni = base.Frase.objects.filter()
    if args.get('id'):
        print('faccio {id}'.format(**args))
        lista_canzoni = [i for i in lista_canzoni if i.id_frase == int(args['id'])]
    else:
        svuota_cartelle('%s/lettere' % (settings.DOCDIR))
    for brano in lista_canzoni:
        doc.genera_lettera(brano.__dict__)


def svuota_cartelle(cartella):
    folder = cartella
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

