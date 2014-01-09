from . import exceptions


def type_of_boolean(type_of):
    def inner(self):
        return self.type_of == type_of
    return property(inner)


def require_initialization(func):
    def inner(self, *args, **kwargs):
        if not self._initialized:
            raise exceptions.NotYetInitialized
        return func(self, *args, **kwargs)
    return property(inner)
