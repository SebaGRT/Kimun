import re

with open('templates/evaluaciones/evaluacion_form.html', 'r') as f:
    content = f.read()

# Fix h1
content = re.sub(r'<h1 class="text-3xl font-bold mt-2">', r'<h1 class="section-title">', content)
# Fix form wrapper
# Right now it's <form ... class="space-y-6">
# Let's change the parent div or the form to be the hybrid-card. 
# "Use hybrid-card wrapper for the main form container"
content = re.sub(r'<form method="post" id="evaluacionForm" class="space-y-6"', 
                 r'<form method="post" id="evaluacionForm" class="hybrid-card rounded-2xl p-8 space-y-6"', 
                 content)

# Remove hybrid-card from the internal divs so we don't have cards in cards, which looks bad.
# Wait, maybe they wanted cards in cards? "Use `hybrid-card` wrapper for the main form container".
# If I wrap the form, the internal ones might be better as just divs with border-subtle or similar.
# But keeping them is also fine. Let's remove the internal hybrid-card class to flatten it, or change to something lighter.
content = content.replace('class="hybrid-card rounded-xl p-6"', 'class="rounded-xl p-6 border border-subtle"')
# also the dynamic question cards have `style="background-color: var(--color-bg); border: 1px solid var(--color-border);"`
# let's change them to `class="mb-6 p-6 rounded-xl border border-subtle bg-surface"`
content = re.sub(r'<div class="mb-6 p-4 rounded-lg" style="background-color: var\(--color-bg\); border: 1px solid var\(--color-border\);">',
                 r'<div class="mb-6 p-6 rounded-xl border border-subtle surface-panel">', content)

# also change text-lg font-semibold to section-title for h2?
# "Add section-title for form section headers"
content = re.sub(r'<h2 class="text-lg font-semibold mb-4">', r'<h2 class="section-title text-xl">', content)
content = re.sub(r'<h2 class="text-lg font-semibold">', r'<h2 class="section-title text-xl">', content)

with open('templates/evaluaciones/evaluacion_form.html', 'w') as f:
    f.write(content)
