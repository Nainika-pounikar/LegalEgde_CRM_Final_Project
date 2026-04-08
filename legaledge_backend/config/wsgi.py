"""
WSGI config for LegalEdge CRM backend.
"""
import os

from django.core.wsgi import get_wsgi_application

from config.deploy_guards import run_startup_guards


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
run_startup_guards()
