# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from .data import setup_data


class Migration(migrations.Migration):

    dependencies = [
        ('igecas', '0001_initial'),
    ]

    operations = [migrations.RunPython(setup_data),
    ]
