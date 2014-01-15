from django.db import models


class MaxCharField(models.CharField):
    def __init__(self, **kwargs):
        kwargs['max_length'] = 250
        super(MaxCharField, self).__init__(**kwargs)


class OptionalMaxCharField(MaxCharField):
    def __init__(self, **kwargs):
        kwargs.update({
            'null': True,
            'blank': True,
        })
        super(OptionalMaxCharField, self).__init__(**kwargs)


# Provide South with the information required to process custom fields.
#
# This fails quietly if there is an ``ImportError`` as it none of this
# matters if South isn't installed.
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^tx_tecreports\.fields\..*Field"])
except ImportError:
    pass
