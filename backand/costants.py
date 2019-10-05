from datetime import datetime
from time import gmtime, strftime

due_date = '2021-07-17'
due_date_umana = datetime.strptime(due_date, "%Y-%m-%d").strftime("%d-%m-%Y")

numero_partecipanti_default = 1

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


</script>"""

delta_days = datetime.strptime(due_date, "%Y-%m-%d") - datetime.today()
delta_days = delta_days.days

def_usr_data = {
    'row_id': 0,
    'nome': '',
    'albergo': 'checked',
    'viaggio': '',
    'menu_sel': '',
    'note': '',
    'foto': '',
}

blocco_righe_invitato = """
    <div class="row" id="riga_invitato#{row_id}">
            <div class="col-sm-1"> Nome </div>
            <div class="col-sm-1">
                	<div class="form-group">
        	        	<input type="text" value="{nome}" placeholder="Inactive" class="form-control" />
                	</div>
            </div>
            <div class="col-sm-1"> Albergo: </div>
            <div class="col-sm-1">
                	<div class="switch"
                          data-on-label="<i class='fa fa-check'></i>"
                          data-off-label="<i class='fa fa-times'></i>">
                          <input type="checkbox" {albergo}/>
                    </div>
            </div>
            <div class="col-sm-1"> Viaggio: </div>
            <div class="col-sm-1">
                	<div class="switch"
                          data-on-label="<i class='fa fa-check'></i>"
                          data-off-label="<i class='fa fa-times'></i>">
                          <input type="checkbox" {viaggio} />
                    </div>
            </div>
            <div class="col-sm-1"> Menu </div>
            <div class="col-sm-2">
                	<div class="form-group">
        	        	<input type="text" value="{menu_sel}" placeholder="Inactive" class="form-control" />
                	</div>
            </div>
            <div class="col-sm-1">Note</div>
            <div class="col-sm-2">
                	<div class="form-group">
        	        	<input type="text" value="{note}" placeholder="note"  class="form-control" />
                	</div>
            </div>
    </div>
""".format(**def_usr_data)

blocco_righe_invitato = """
    <div class="row" id="riga_invitato#{row_id}">

            <div class="col-sm-2">
                    <img src="assets/img/mockup.png" alt="Circle Image" class="img-circle">

                </div>
            <div class="col-md-10">
                <div class="row">
                    <div class="col-sm-1"> Nome: </div>
                    <div class="col-sm-3">
                            <div class="form-group">
                                <input type="text" value="{nome}" placeholder="Inactive" class="form-control" />
                            </div>
                    </div>
                    <div class="col-sm-1"> Albergo: </div>
                    <div class="col-sm-1">
                            <div class="switch"
                                  data-on-label="<i class='fa fa-check'></i>"
                                  data-off-label="<i class='fa fa-times'></i>">
                                  <input type="checkbox" {albergo}/>
                            </div>
                    </div>
                    <div class="col-sm-1"> Albergo: </div>
                    <div class="col-sm-1">
                            <div class="switch"
                                  data-on-label="<i class='fa fa-check'></i>"
                                  data-off-label="<i class='fa fa-times'></i>">
                                  <input type="checkbox" {albergo}/>
                            </div>
                    </div>
                    <div class="col-sm-1"> Viaggio: </div>
                    <div class="col-sm-1">
                            <div class="switch"
                                  data-on-label="<i class='fa fa-check'></i>"
                                  data-off-label="<i class='fa fa-times'></i>">
                                  <input type="checkbox" {viaggio} />
                            </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm-1"> Menu </div>
                    <div class="col-sm-3">
                            <div class="form-group">
                                <input type="text" value="{menu_sel}" placeholder="Inactive" class="form-control" />
                            </div>
                    </div>
                    <div class="col-sm-1">Note</div>
                    <div class="col-sm-3">
                            <div class="form-group">
                                <input type="text" value="{note}" placeholder="note"  class="form-control" />
                            </div>
                    </div>
                    <div class="col-sm-1">Foto:</div>
                    <div class="col-sm-3">
                            <div class="form-group">
                                <input type="text" value="{note}" placeholder="note"  class="form-control" />
                            </div>
                    </div>
                </div>
            </div>
    </div>
""".format(**def_usr_data)

def get_costants():
    return globals()