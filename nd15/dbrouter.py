class DBRouter(object):
    """
    A router to control nd15 db operations
    """
    def db_for_read(self, model, **hints):
        "Point all operations on nd15 models to 'db_nd15'"
        from django.conf import settings
        if not 'db_nd15' in settings.DATABASES:
            return None
        if model._meta.app_label == 'nd15':
            return 'db_nd15'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on nd15 models to 'db_nd15'"
        from django.conf import settings
        if not 'db_nd15' in settings.DATABASES:
            return None
        if model._meta.app_label == 'nd15':
            return 'db_nd15'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in nd15 is involved"
        from django.conf import settings
        if not 'db_nd15' in settings.DATABASES:
            return None
        if obj1._meta.app_label == 'nd15' or obj2._meta.app_label == 'nd15':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the nd15 app only appears on the 'nd15' db"
        from django.conf import settings
        if not 'db_nd15' in settings.DATABASES:
            return None
        if db == 'db_nd15':
            return model._meta.app_label == 'nd15'
        elif model._meta.app_label == 'nd15':
            return False
        return None