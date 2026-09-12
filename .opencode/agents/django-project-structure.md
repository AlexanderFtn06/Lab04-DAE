---
description: Create Django project with course structure, install Pillow, declare library app in INSTALLED_APPS
mode: subagent
tools: write, edit, bash
---

# Django Project Structure Agent

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

## Step 1: Create Project Structure

1. Create Django project with standard structure:
   - Project folder: `config/`
   - App: `library/` (singular model names)
   
2. Install Pillow:
   ```bash
   pip install Pillow
   ```

3. Add `library` to INSTALLED_APPS in `config/settings.py`

4. Verify structure:
   ```
   project/
   ├── config/
   │   ├── __init__.py
   │   ├── settings.py
   │   ├── urls.py
   │   └── wsgi.py
   ├── library/
   │   ├── __init__.py
   │   ├── models.py
   │   ├── admin.py
   │   ├── apps.py
   │   └── migrations/
   └── manage.py
   ```

Before executing, check current directory structure to respect cumulative nature.