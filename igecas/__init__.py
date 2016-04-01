"""IGECAS
Individual Genetical, Environmental and Calculated Attribute Store.
"""

from django.apps import AppConfig

class IGECAS(AppConfig):
    name = 'igecas'
    verbose_name = "IGECAS"


default_app_config = "igecas.IGECAS"


"""
guuid
-----
:


label
-----
value = rs12913832


label_type
----------
label = label





data
----
dts_insert 
dts_update
dts_remove

guuid = 
label = rs12913832
value = 'gg'





def example(rs12913832):
    value = Value(name="eye_colour", confidence=80, prevalence=None)
    return value

"""
