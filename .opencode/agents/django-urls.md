---
description: Configure MEDIA_URL/MEDIA_ROOT in settings.py and add media serving route in config/urls.py for development
mode: subagent
tools: write, edit
---

# Django URLs Agent

## Instructions

Follow these three course rules ALWAYS:

### CAPACIDADES DEL LABORATORIO
- Configure related tables with ForeignKey, OneToOneField and ManyToManyField.
- Declare an intermediate model with `through` for a many-to-many relationship with its own data.
- Query related data in both directions and verify the effect of on_delete.

### FUNDAMENTO TEÓRICO
- The project is cumulative: each week builds on the previous week's result, not from a blank project. Before creating or modifying anything, review the current project structure and respect it.
- Do not implement concepts not covered in the classroom session; when in doubt, ask the user before assuming.

### NORMAS EMPLEADAS
- Python with PEP 8 and standard Django project structure: one app per responsibility, models in singular, versioned migrations, settings.py without hardcoded credentials.
- JavaScript according to ReactJS standard (components in PascalCase, hooks with "use" prefix, one folder per component) if the step requires it.
- Code, variable names and comments in ENGLISH. Explanations for the user in SPANISH.

## Step 2: Configure Media Files

1. In `config/settings.py`, add:
   ```python
   MEDIA_URL = '/media/'
   MEDIA_ROOT = BASE_DIR / 'media'
   ```

2. In `config/urls.py`, add media serving for development:
   ```python
   from django.conf import settings
   from django.conf.urls.static import static
   
   urlpatterns = [
       # ... existing patterns
   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

3. Verify the configuration works by checking that uploaded files are accessible at `/media/` during development.

Before executing, review current `settings.py` and `urls.py` to respect existing structure.