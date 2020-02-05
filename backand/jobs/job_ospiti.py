from matrimonio.backand.bo import base, doc

def main(args):
    crea_hash()
    crea_hash()

def crea_hash():
    elenco_famiglie = base.Famiglia.objects.filter()
    for famiglia in elenco_famiglie:
        if not famiglia.hash:
            famiglia.calcola_hash()
        famiglia.genera_partecipazione()

def crea_segnaposto():
    elenco_ospiti = base.Ospite.objects.filter()
    print(elenco_ospiti)
    doc.genera_segnaposto([i.nome for i in elenco_ospiti])
    doc.genera_copertina()
    pass
