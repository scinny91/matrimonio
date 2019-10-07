from django.http import JsonResponse
import traceback
import costants

global res

def main(request):
    res = {
        'result': [],
        'errori': [],
        'warning': [],
        'logs': str(request.__dict__),
        'logs': '',
    }


    try:
        action = request.POST.get('action', request.GET.get('action', ''))
        res['result'] = action

        if not action:
            raise ValueError('action non specificata, esco')

        import sys
        diz = {'logs': None}
        diz.update(request.POST)
        diz.update(request.GET)
        res['result'] = getattr(sys.modules[__name__], action)(diz)

    except Exception:
        res['warning'] = []
        res['result'] = []
        res['errori'] = traceback.format_exc()


    return JsonResponse(res)


def add_guest(diz_in):
    html = costants.blocco_righe_invitato

    html.format(**{'row_id': diz_in['index']})

    return html.format(**{'row_id': diz_in['index']})