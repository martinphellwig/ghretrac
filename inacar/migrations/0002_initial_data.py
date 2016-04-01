# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import  migrations

from .data import setup_data


class Migration(migrations.Migration):

    dependencies = [
        ('inacar', '0001_initial'),
    ]

    operations = [migrations.RunPython(setup_data),
    ]
