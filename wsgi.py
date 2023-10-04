import os
from django.core.wsgi import get_wsgi_application

# Configura la variable de entorno para usar la configuración de tu proyecto Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")

# Carga la aplicación WSGI de Django
application = get_wsgi_application()