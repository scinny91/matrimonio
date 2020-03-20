from datetime import datetime
from time import gmtime, strftime
from matrimonio import settings
import git
import traceback

def get_version():
    try:
        repo = git.Repo(search_parent_directories=False, path=settings.GITFILE)
        return str(repo.head.object.hexsha)
    except:
        print(traceback.format_exc())
        return 'git info not found'

version = get_version()


appserver = settings.APPSERVER
hash = 'undef'

due_date = '2021-07-10'
due_date_umana = datetime.strptime(due_date, "%Y-%m-%d").strftime("%d-%m-%Y")
delta_days = datetime.strptime(due_date, "%Y-%m-%d") - datetime.today()
delta_days = delta_days.days

js_index = """

<script type="text/javascript">

    $('.btn-tooltip').tooltip();
    $('.label-tooltip').tooltip();
    $('.pick-class-label').click(function(){
        var new_class = $(this).attr('new-class');
        var old_class = $('#display-buttons').attr('data-class');
        var display_div = $('#display-buttons');
        if(display_div.length) {
        var display_buttons = display_div.find('.btn');
        display_buttons.removeClass(old_class);
        display_buttons.addClass(new_class);
        display_div.attr('data-class', new_class);
        }
    });
    $( "#slider-range" ).slider({
		range: true,
		min: 0,
		max: 500,
		values: [ 75, 300 ],
	});
	$( "#slider-default" ).slider({
			value: 70,
			orientation: "horizontal",
			range: "min",
			animate: true
	});
	$('.carousel').carousel({
      interval: 4000
    });


</script>
"""

def_usr_data = {
    'id_ospite': 0,
    'nome': '',
    'albergo': '',
    'mail': '',
    'menu_sel': '',
    'select_uomo': 'checked',
    'select_donna': '',
    'piede': 0,
    'note': '',
    'foto': '',
    'url_img_user': 'assets/img/mockup.png',
    'select_bambino': '',
    'select_adulto': '',
    'select_senza_glutine': '',
    'select_senza_lattosio': '',
}


blocco_righe_invitato = """
    <div class="row" id="riga_invitato_{id_ospite}">

            <div class="col-sm-3">
                    <div class='delete_ospite'  id='cancella_ospite_{id_ospite}'>
                        <i class="fas fa-user-times"></i>
                    </div>
                    <img src="{url_img_user}" alt="Circle Image" class="img-circle" id='img_{id_ospite}'>
                </div>
            <div class="col-md-9">
                <div class="row">
                    <div class="col-sm-4 lbl">
                        <div class="form-group">
                             <label class="control-label">Nome:</label>
                            <input type="text" value="{nome}" name='nome' placeholder="Digita il nome dell'ospite" class="form-control onchangeupdate" id='nome_ospite_{id_ospite}' />
                        </div>
                    </div>
                    <div class="col-sm-1 lbl">
                        <div class="form-group {mostra_albergo}">
                            <label class="control-label" >Albergo:</label>
                            <div class="switch-unload" id='switchAlbergo_{id_ospite}'  data-on-label="<i class='fa fa-check'></i>" data-off-label="<i class='fa fa-times'></i>">
                                  <input type="checkbox" {albergo} id='albergo_{id_ospite}' class='onchangeupdate'  name='albergo'/>
                            </div>
                        </div>
                    </div>
                    <div class="col-sm-3 lbl">
                        <div class="form-group">
                            <label class="control-label">Mail:</label>
                            <input type="text" value="{mail}" name='mail' placeholder="Inserisci un indirizzo mail" class="form-control onchangeupdate" id='mail_{id_ospite}' />
                        </div>
                    </div>
                    <div class="col-sm-2 lbl">
                        <div class="form-group">
                            <label class="control-label">Sesso:</label>
                            <select class="form-control onchangeupdate" id="sesso_{id_ospite}" name='sesso'>
                                  <option {select_uomo} value='Uomo'>Uomo</option>
                                  <option {select_donna} value='Donna'>Donna</option>
                            </select> 
                        </div>
                    </div>
                    <div class="col-sm-2 lbl">
                        <div class="form-group">
                            <label class="control-label">Numero scarpa:</label>
                            <input type="text" value="{piede}" name='piede' placeholder="" class="form-control onchangeupdate" id='piede_{id_ospite}' />
                        </div>
                    </div>


                </div>
                <div class="row">
                    <div class="col-sm-4 lbl">
                        <div class="form-group">
                            <label class="control-label">Menu:</label>
                            <select class="form-control onchangeupdate" id="menu_{id_ospite}" name='menu'>
                                  <option {select_bambino} value='bambino'>Bambino</option>
                                  <option {select_adulto} value='adulto'>Carne</option>
                                  <option {select_senza_glutine} value='senza_glutine'>Senza glutine</option>
                                  <option {select_senza_lattosio} value='senza_lattosio'>Senza lattosio</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-sm-4 lbl">
                          <label class="control-label">Note:</label>
                         <textarea class="form-control onchangeupdate" id="note_{id_ospite}" rows="2" name='note'></textarea>
                    </div>
                    <div class="col-sm-4 lbl">
                        <label class="control-label">Foto:</label>
                        <input type="file" class="form-control-file" id="foto_{id_ospite}" onchange='uploadFile(this)'>
                    </div>
                </div>
            </div>
    </div>
"""


def get_costants():
    return globals()