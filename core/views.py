from django.http import HttpResponse


def index(requests):
    return HttpResponse(f'hello jorrrld')

