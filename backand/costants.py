from datetime import datetime
from time import gmtime, strftime
from matrimonio import settings


appserver = settings.APPSERVER

due_date = '2021-07-10'
due_date_umana = datetime.strptime(due_date, "%Y-%m-%d").strftime("%d-%m-%Y")

numero_ospiti_default = 1

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

delta_days = datetime.strptime(due_date, "%Y-%m-%d") - datetime.today()
delta_days = delta_days.days

def_usr_data = {
    'id_ospite': 0,
    'nome': '',
    'albergo': '',
    'mail': '',
    'viaggio': '',
    'menu_sel': '',
    'note': '',
    'foto': '',
    'url_img_user': 'assets/img/mockup.png',
}



blocco_righe_invitato = """
    <div class="row" id="riga_invitato#{id_ospite}">

            <div class="col-sm-3">
                    <i class="fas fa-user-times delete_ospite" id='cancella_ospite_{id_ospite}'></i>
                    <img src="{url_img_user}" alt="Circle Image" class="img-circle" id='img_{id_ospite}'>

                </div>
            <div class="col-md-9">
                <div class="row">
                    <div class="col-sm-1 lbl"> Nome: </div>
                    <div class="col-sm-3 lbl">
                        <div class="form-group">
                            <input type="text" value="{nome}" name='nome' placeholder="Digita il nome dell'ospite" class="form-control onchangeupdate" id='nome_ospite_{id_ospite}' />
                        </div>
                    </div>
                    <div class="col-sm-1 lbl"> Albergo: </div>
                    <div class="col-sm-1 lbl">
                        <div class="switch-unload" id='switchAlbergo_{id_ospite}'  data-on-label="<i class='fa fa-check'></i>" data-off-label="<i class='fa fa-times'></i>">
                              <input type="checkbox" {albergo} id='albergo_{id_ospite}' class='onchangeupdate'  name='albergo'/>
                        </div>
                    </div>
                     <div class="col-sm-1 lbl"> Mail: </div>
                    <div class="col-sm-3 lbl">
                        <div class="form-group">
                            <input type="text" value="{mail}" name='mail' placeholder="Inserisci un indirizzo mail" class="form-control onchangeupdate" id='mail_{id_ospite}' />
                        </div>
                    </div>
                   
                    <div class="col-sm-1 lbl" > Viaggio: </div>
                    <div class="col-sm-1 lbl">
                        <div class="switch-unload" id='switchViaggio_{id_ospite}' data-on-label="<i class='fa fa-check'></i>" data-off-label="<i class='fa fa-times'></i>">
                              <input type="checkbox" {viaggio} id='viaggio_{id_ospite}' class='onchangeupdate' name='viaggio'/>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm-1 lbl"> Menu </div>
                    <div class="col-sm-3 lbl">
                        <div class="form-group">
                            <select class="form-control onchangeupdate" id="menu_{id_ospite}" name='menu'>
                                  <option>Bambino</option>
                                  <option>Carne</option>
                                  <option>Pesce</option>
                                  <option>Carne (senza glutine)</option>
                                  <option>Pesce (senza glutine)</option>
                                  <option>Carne (senza lattosio)</option>
                                  <option>Pesce (senza lattosio)</option>
                                </select>  
                        </div>
                    </div>
                    <div class="col-sm-1 lbl" >Note</div>
                    <div class="col-sm-3 lbl">
                         <textarea class="form-control onchangeupdate" id="note_{id_ospite}" rows="2" name='note'></textarea>
                    </div>
                    <div class="col-sm-1 lbl">Foto:</div>
                    <div class="col-sm-3 lbl">
                        <input type="file" class="form-control-file" id="foto_{id_ospite}" onchange='uploadFile(this)'>
                    </div>
                </div>
            </div>
    </div>
"""
index_blocco_righe_invitato = blocco_righe_invitato.format(**def_usr_data)

def get_costants():
    return globals()