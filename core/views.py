from django.http import HttpResponse

from lys import L

from ns import models as ns_models
from nd15 import models as nd15_models

from .templates import stream as templates_stream


def index(requests):
    links = []
    for parl in nd15_models.Parlementaire.objects.all().order_by('nom_de_famille'):
        links.append(L.li / L.a(href=parl.slug + '/') / parl.nom)
    return HttpResponse(L.ul / links)


def parl(requests, slug):
    parl = nd15_models.Parlementaire.objects.get(slug=slug)

    events = []
    if requests.GET.get('filter', 'votes') == 'votes':
        for vote in nd15_models.ParlementaireScrutin.objects.filter(parlementaire_id=parl).order_by('-scrutin__numero'):
            events.append({
                'date': str(vote.scrutin.date),
                'type': 'Vote',
                'content': f'A voté <b>{vote.position}</b> sur {vote.scrutin.titre}',
                'url': f'https://www.nosdeputes.fr/15/scrutin/{vote.scrutin.numero}'
            })
    if requests.GET.get('filter', 'votes') == 'interventions':
        for inter in nd15_models.Intervention.objects.filter(parlementaire_id=parl.id):
            events.append({
                'date': str(inter.date),
                'type': 'Intervention',
                'content': '<i>'+inter.intervention+'</i>',
                'url': f"https://nosdeputes.fr/15/seance/{inter.seance_id}#inter_{inter.md5}"
            })
    events.sort(key=lambda event:event['date'])
    events = list(reversed(events))

    html = templates_stream.render(requests, events)
    html = html.replace('Paula Forteza', parl.nom)
    html = html.replace('XXX', parl.nom_circo)
    if parl.sexe == 'F':
        html = html.replace('Député', 'Députée')

    return HttpResponse(html)