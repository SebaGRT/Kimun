import os

# Set Django settings module before importing Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kimun.settings')

# Import the WSGI application from the Django project
from kimun.wsgi import application

# Vercel Python runtime expects the WSGI callable to be named 'app'
app = application
