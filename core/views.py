from django.http import HttpResponse
from django.middleware.csrf import get_token

from lys import L

from ns import models as ns_models
from nd15 import models as nd15_models
from .models import Follow
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
        for vote in nd15_models.ParlementaireScrutin.objects.filter(parlementaire_id=parl).order_by('-scrutin__numero').select_related('scrutin'):
            if not vote.position:
                continue
            events.append({
                'date': vote.scrutin.date,
                'type': 'Vote',
                'content': f'A voté <b>{vote.position}</b> sur {vote.scrutin.titre}',
                'url': f'https://www.nosdeputes.fr/15/scrutin/{vote.scrutin.numero}'
            })
    if requests.GET.get('filter') in (None, 'interventions', 'questions-orales'):
        for inter in nd15_models.Intervention.objects.filter(parlementaire_id=parl.id):
            if requests.GET.get('filter') == 'interventions' and inter.type == 'question':
                continue
            if requests.GET.get('filter') == 'questions-orales' and not inter.type == 'question':
                continue
            events.append({
                'date': inter.date,
                'type': 'Intervention' + (' - Question orale' if inter.type == 'question' else ''),
                'content': inter.intervention,
                'url': f"https://nosdeputes.fr/15/seance/{inter.seance_id}#inter_{inter.md5}"
            })
    if requests.GET.get('filter', 'amendements') == 'amendements':
        for amdt in nd15_models.Amendement.objects.filter(auteur_id=parl.id):
            if not amdt.date:
                continue
            if not amdt.expose:
                continue
            events.append({
                'date': amdt.date,
                'type': 'Amendement (Auteur)',
                'content': amdt.expose,
                'url': f"https://nosdeputes.fr/15/amendement/{amdt.texteloi_id}/{amdt.numero}"
            })
    if requests.GET.get('filter') in (None, 'rapports', 'propositions-de-loi'):
        for signature in nd15_models.ParlementaireTexteloi.objects.filter(parlementaire=parl):
            rapport = signature.texteloi.type not in ('Proposition de loi', 'Proposition de résolution')
            if requests.GET.get('filter') == 'rapports' and not rapport:
                continue
            if requests.GET.get('filter') == 'propositions-de-loi' and rapport:
                continue
            events.append({
                'date': signature.texteloi.date,
                'type': signature.texteloi.type + (' (Auteur)' if signature.importance == 1 else ''),
                'content': f"{signature.texteloi.type} {signature.texteloi.titre}",
                'url': f"https://nosdeputes.fr/15/document/{signature.texteloi.id}"
            })
    if requests.GET.get('filter', 'questions-ecrites') == 'questions-ecrites':
        for question in nd15_models.QuestionEcrite.objects.filter(parlementaire=parl):
            events.append({
                'date': question.date,
                'type': 'Question écrite',
                'content': question.question,
                'url': f"https://nosdeputes.fr/15/question/QE/{question.numero}"
            })
    events.sort(key=lambda event:event['date'])
    events = list(reversed(events))

    html = templates_stream.render(requests, events)
    html = html.replace('YYY', parl.nom)
    html = html.replace('XXX', parl.nom_circo)
    html = html.replace('ZZZ', parl.slug)
    html = html.replace('GGG', parl.groupe_acronyme)
    html = html.replace('TTT', get_token(requests))
    if parl.sexe == 'F':
        html = html.replace('Député', 'Députée')

    return HttpResponse(html)

def follow(requests):
    email = requests.POST['email']
    slug = requests.POST['slug']
    follow = Follow(parlementaire_slug=slug, email=email)
    follow.save()
    return HttpResponse('ok')