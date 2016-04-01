from django.contrib import admin
from . import models 
from inspect import isclass
# Register your models here.

for name in dir(models):
    subject = getattr(models, name)
    if isclass(subject) and issubclass(subject, models._Abstract):
        if not name.startswith('_'):
            admin.site.register(subject)