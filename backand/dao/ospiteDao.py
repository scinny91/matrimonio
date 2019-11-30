from django.db import connection
import MySQLdb
import pprint
from matrimonio import settings

def mysql_update(sql):
    # Connessione al Database
    db = MySQLdb.connect(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['USER'], settings.DATABASES['default']['PASSWORD'], settings.DATABASES['default']['NAME'])
    # Ottenimento del cursore
    cursor = db.cursor()
    # Esecuzione di una query SQL
    cursor.execute("SELECT VERSION()")
    # Lettura di una singola riga dei risultati della query
    data = cursor.fetchone()
    # Disconnessione
    db.close()

    with connection.cursor() as cursor:
        print (cursor.execute(sql))
    return ''

def mysql_select(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
    print(sql)
    return cursor.fetchall()


def crea_ospite(ospite):
    pprint.pprint(ospite)
    sql = """
    INSERT INTO `ospiti` (`nome`, `note`, `id_famiglia`, `speciale`)
    VALUES ("{nome_ospite}", "{note}", {id_famiglia}, "{speciale}")
    """.format(**ospite)
    print(sql)
    print(settings.DATABASES['default'])
    mysql_update(sql)
    return mysql_update(sql)


def create_famiglia(famiglia):
    sql = """
    insert into famiglie """




