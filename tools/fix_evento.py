import re

with open('templates/calendario/evento_form.html', 'r') as f:
    content = f.read()

content = re.sub(
    r'<div class="mt-6 p-4 rounded-xl" style="background-color: #fee2e2; color: #dc2626;">',
    r'<div class="mt-6 p-4 rounded-xl bg-red-50 text-red-700 border border-red-200">',
    content
)

with open('templates/calendario/evento_form.html', 'w') as f:
    f.write(content)
