"""
WSGI config for dosteps project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

import django
django.setup()

from django.contrib.auth.models import User

user = User.objects.get_or_create(username='admin', 
                                 is_superuser=True, is_staff=True)[0]
user.set_password('admin')
user.save()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
