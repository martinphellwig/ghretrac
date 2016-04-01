"""INACAR
Identity, Name Address Contact and Relation
"""

from django.apps import AppConfig

class INACAR(AppConfig):
    "The AppConfig for Identity, Name, Address, Contact and Relation"
    name = 'inacar'
    verbose_name = "INACAR"

    def ready(self):
        from . import signals
        AppConfig.ready(self)

default_app_config = "inacar.INACAR"