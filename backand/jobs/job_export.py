import MySQLdb
import pprint
from matrimonio import settings

TABELLE = ['frasi', 'ospiti', 'famiglie','foto','commenti']

file_dump = settings.DOCDIR + '/dump.sql'


def main(args):
    file = open(file_dump, 'w')
    file.write('')
    file.close()
    for tabella in TABELLE:
        create(tabella)
        insert(tabella)


def create(tabella):
    sql = 'Show create table %s' % tabella
    create_table = mysql_query(sql)


    file = open(file_dump, 'a')
    file.write(create_table[0][1])
    file.close()

def insert(tabella):


    sql = 'DESC %s' % tabella
    desc = mysql_query(sql)

    elenco_campi = [i[0] for i in desc]



    sql = 'select * from  %s' % tabella
    dati = mysql_select(sql)
    if not dati:
        print('tabella vuota')
        return
    sql = []
    for riga in dati:
        sql.append("""('%s')""" % "', '".join([str(riga[i]) for i in elenco_campi]))

    sql = [''',
'''.join(sql)]
    sql.insert(0, """
INSERT INTO %s ('%%s')
    """ % tabella % "','".join(elenco_campi))
    sql.append(';')

    file = open(file_dump, 'a')
    file.write(''.join(sql))
    file.close()



def mysql_select(sql):
    db = MySQLdb.connect(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['USER'], settings.DATABASES['default']['PASSWORD'], settings.DATABASES['default']['NAME'])
    # Ottenimento del cursore
    #cursor = db.cursor()
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    # Esecuzione di una query SQL
    cursor.execute(sql)
    # Lettura di una singola riga dei risultati della query
    data = cursor.fetchall()
    # Disconnessione
    db.close()
    return data


def mysql_query(sql):
    db = MySQLdb.connect(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['USER'], settings.DATABASES['default']['PASSWORD'], settings.DATABASES['default']['NAME'])
    # Ottenimento del cursore
    cursor = db.cursor()
    # Esecuzione di una query SQL
    cursor.execute(sql)
    # Lettura di una singola riga dei risultati della query
    data = cursor.fetchall()
    # Disconnessione
    db.close()
    return data