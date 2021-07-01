from datetime import datetime
from time import gmtime, strftime
import os
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
delta_days = max(delta_days.days, 0)

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
	


</script>
"""




def get_costants():
    return globals()

