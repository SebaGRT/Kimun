import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kimun.settings")
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()
try:
    user = User.objects.get(username="admin")
except:
    user = User.objects.create_superuser("admin", "admin@admin.com", "admin123")

c = Client()
c.force_login(user)

for url in ["/", "/reportes/", "/cursos/", "/tareas/", "/evaluaciones/", "/calendario/"]:
    response = c.get(url)
    if response.status_code != 200:
        print(f"Error on {url}: {response.status_code}")
        # Look for the error message in the response
        content = response.content.decode()
        if "Exception" in content or "Error" in content:
            import re
            match = re.search(r'Exception Value:.*?</pre>', content, re.DOTALL)
            if match:
                print(match.group(0))
            else:
                print("Could not parse exception.")
