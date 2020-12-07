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
    return HttpResponse(templates_stream.TEMPLATE)