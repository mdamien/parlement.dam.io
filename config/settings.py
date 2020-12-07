from .base_settings import *

INSTALLED_APPS += [
    'core',
    'nd15',
    'ns'
]

DATABASE_ROUTERS = [
    'nd15.dbrouter.DBRouter',
    'ns.dbrouter.DBRouter',
]

DATABASES['db_nd15'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'cpc',
    'USER': 'cpc',
    'PASSWORD': 'password',
}

DATABASES['db_ns'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'cpc_ns',
    'USER': 'cpc',
    'PASSWORD': 'password',
}