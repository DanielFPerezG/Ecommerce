"""
WSGI config for ecommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""
from django.contrib.auth.handlers.modwsgi import check_password, groups_for_user
from django.core.handlers.wsgi import WSGIHandler
import os

from django.core.wsgi import get_wsgi_application


os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

application = WSGIHandler()