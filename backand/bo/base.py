from django.db import models



"""class Colore(models.Model):

    colore = models.IntegerField(max_length=11, primary_key=True)
    articolo = models.ManyToManyField('Articolo', blank=True, through='ColoreArticolo')

    class Meta:
        db_table = 'prova_colori_cim'
        app_label = 'cim'
        ordering = ('colore',)

    #objects = ColoreManager()"""



class Ospite(models.Model):

    choices = [
        ('S','on'),
        ('N','off'),
    ]

    id_ospite = models.AutoField(max_length=11, primary_key=True)
    nome = models.Field(name='nome', blank=True)
    speciale = models.CharField(max_length=1, choices=choices)
    albergo = models.CharField(max_length=1, choices=choices)
    mail = models.CharField(max_length=100, blank=True)
    viaggio = models.CharField(max_length=1, choices=choices)
    note = models.Field(blank=True)
    url_img_user = models.Field(blank=True, default='assets/img/mockup.png')
    menu = models.Field(blank=True)
    cod_famiglia = models.Field(blank=True)
    utente = models.Field(blank=True)

    class Meta:
        db_table = 'ospiti'
        app_label = 'matrimonio'

    def toHtml(self):
        check_fields = ['albergo', 'viaggio']
        for item in check_fields:
            value = self.__getattribute__(item)
            self.__setattr__(item, '' if value == 'N' else 'checked')
        return self.__dict__