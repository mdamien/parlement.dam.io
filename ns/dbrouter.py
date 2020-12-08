class DBRouter(object):
    """
    A router to control ns db operations
    """
    def db_for_read(self, model, **hints):
        "Point all operations on ns models to 'db_ns'"
        if model._meta.app_label == 'ns':
            return 'db_ns'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on ns models to 'db_ns'"
        if model._meta.app_label == 'ns':
            return 'db_ns'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in ns is involved"
        if obj1._meta.app_label == 'ns' or obj2._meta.app_label == 'ns':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the ns app only appears on the 'ns' db"
        if db == 'db_ns':
            return model._meta.app_label == 'ns'
        elif model._meta.app_label == 'ns':
            return False
        return None