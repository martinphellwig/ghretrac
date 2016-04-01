"""
We just simply add all models in the admin interface.
"""

#pylint: disable=locally-disabled, protected-access

from django.contrib import admin
from . import models
from inspect import isclass
from django.contrib.admin.sites import AlreadyRegistered

@admin.register(models.UUID)       
class UUIDAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'uuid', 'poid')

# Now register the remaining
for name in dir(models):
    registee = list()
    subject = getattr(models, name)
    if isclass(subject) and issubclass(subject, models._Abstract):
        if not name.startswith('_'):
            try:
                admin.site.register(subject)
            except AlreadyRegistered:
                pass

    

