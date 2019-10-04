
from django.http import HttpResponse
from django.contrib.staticfiles.templatetags import staticfiles
from datetime import datetime
from time import gmtime, strftime


def start(request):

    url = request.META['PATH_INFO']

    html = ''
    if url == '/html/':
        with open('matrimonio/html/index.html', 'r') as content_file:
            html = content_file.read()
            dati_dinamici = {
                'delta_days': (datetime.strptime('2021-07-21', "%Y-%m-%d") -
                                datetime.strptime(strftime("%Y-%m-%d", gmtime()), "%Y-%m-%d")).days,
                'js_index': js_index,
            }
            html = html.format(**dati_dinamici)
    else:
        with open('matrimonio/%s' % url, 'r') as content_file:
            html = content_file.read()
    if '.js' in url:
        return HttpResponse(html, content_type="application/x-javascript")
    elif '.css' in url:
        return HttpResponse(html, content_type="text/css")
    else:
       return HttpResponse(html)


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