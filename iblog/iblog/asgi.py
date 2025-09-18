"""
ASGI config for iblog project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

profile = os.environ.get('IBLOG_PROFILE', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "iblog.settings.%s" % profile)

application = get_asgi_application()
