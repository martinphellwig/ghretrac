"""
We just simply add all models in the admin interface.
"""

#pylint: disable=locally-disabled, protected-access

from django.contrib import admin
from . import models
from inspect import isclass

for name in dir(models):
    registee = list()
    subject = getattr(models, name)
    if isclass(subject) and issubclass(subject, models._Abstract):
        if not name.startswith('_'):
            admin.site.register(subject)

