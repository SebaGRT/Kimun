import os
import sys

# Add the project root to Python path so we can import kimun
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set Django settings BEFORE importing WSGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kimun.settings')

# Now import and create the WSGI application
from django.core.wsgi import get_wsgi_application

_django_app = get_wsgi_application()

def _convert_headers(headers):
    """Convert any bytes header keys/values to strings."""
    result = []
    for key, value in headers:
        if isinstance(key, bytes):
            key = key.decode('latin-1')
        if isinstance(value, bytes):
            value = value.decode('latin-1')
        result.append((key, value))
    return result

def application(environ, start_response):
    """WSGI application wrapper that fixes byte headers."""
    def _wrapped_start_response(status, headers, exc_info=None):
        fixed_headers = _convert_headers(headers)
        return start_response(status, fixed_headers, exc_info)
    
    return _django_app(environ, _wrapped_start_response)

# Vercel expects 'app' variable for Python serverless functions
app = application
