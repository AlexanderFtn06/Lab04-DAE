---
description: Generate and apply migrations, verify created tables including the intermediate many-to-many table
mode: subagent
tools: bash, read
---

# Django Migrations Agent

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

## Step 7: Generate and Apply Migrations

1. Generate migrations:
   ```bash
   python manage.py makemigrations library
   ```

2. Review the generated migration file to verify:
   - Author, Book, Publisher, Category, AuthorProfile, Publication tables
   - ForeignKey constraints with correct on_delete
   - OneToOneField for AuthorProfile
   - ManyToManyField for Book-Category (creates intermediate table automatically)
   - Through model Publication for Book-Publisher

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. Verify tables in database:
   ```bash
   # SQLite
   python manage.py dbshell
   .tables
   .schema library_author
   .schema library_book
   .schema library_category
   .schema library_publisher
   .schema library_authorprofile
   .schema library_publication
   .schema library_book_categories  # Auto-created M2M table
   .quit
   ```

5. Or use Django ORM to verify:
   ```bash
   python manage.py shell -c "
   from django.db import connection
   print(connection.introspection.table_names())
   "
   ```

Document the output showing all 7 tables created (including library_book_categories and library_publication).