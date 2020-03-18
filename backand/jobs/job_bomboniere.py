from matrimonio.backand.bo import doc, base





def main(args):
    print('Copertine....')
    crea_copertina(args)
    print('Lettere....')
    crea_lettera(args)
    print('Segnposto....')
    crea_segnaposto()

def crea_segnaposto():
    print('creo segnaposto')
    elenco_ospiti = base.Ospite.objects.filter()
    for ospite in elenco_ospiti:
        if ospite.nom:
            doc.genera_segnaposto(ospite.nome)


def crea_copertina(args):
    lista_canzoni = base.Frase.objects.filter()
    if args.get('id'):
        print('faccio {id}'.format(**args))
        lista_canzoni = [i for i in lista_canzoni if i.id_frase == int(args['id'])]
    for brano in lista_canzoni:
        doc.genera_copertina(brano.__dict__)


def crea_lettera(args):
    lista_canzoni = base.Frase.objects.filter()
    if args.get('id'):
        print('faccio {id}'.format(**args))
        lista_canzoni = [i for i in lista_canzoni if i.id_frase == int(args['id'])]
    for brano in lista_canzoni:
        doc.genera_lettera(brano.__dict__)
