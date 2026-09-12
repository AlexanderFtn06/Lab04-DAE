---
description: Load test data via Django admin: 2 authors, 4 books, 3 categories, 2 publishers, with at least one book in 2 categories
mode: subagent
tools: write, edit, bash
---

# Django Admin Agent

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

## Step 8: Load Test Data via Admin

1. Register models in `library/admin.py`:
   ```python
   from django.contrib import admin
   from .models import Author, Book, Publisher, Category, AuthorProfile, Publication
   
   @admin.register(Author)
   class AuthorAdmin(admin.ModelAdmin):
       list_display = ['first_name', 'last_name', 'nationality']
       search_fields = ['first_name', 'last_name']
   
   @admin.register(Book)
   class BookAdmin(admin.ModelAdmin):
       list_display = ['title', 'author', 'isbn', 'publication_date']
       list_filter = ['author', 'categories', 'publishers']
       filter_horizontal = ['categories', 'publishers']
       search_fields = ['title', 'isbn']
   
   @admin.register(Publisher)
   class PublisherAdmin(admin.ModelAdmin):
       list_display = ['name', 'website']
       search_fields = ['name']
   
   @admin.register(Category)
   class CategoryAdmin(admin.ModelAdmin):
       list_display = ['name']
       search_fields = ['name']
   
   @admin.register(AuthorProfile)
   class AuthorProfileAdmin(admin.ModelAdmin):
       list_display = ['author', 'website']
   
   @admin.register(Publication)
   class PublicationAdmin(admin.ModelAdmin):
       list_display = ['book', 'publisher', 'publication_date', 'edition']
       list_filter = ['publisher']
   ```

2. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

3. Run server and access admin at http://127.0.0.1:8000/admin/

4. Create test data:
   - **2 Authors**: 
     - Gabriel García Márquez (Colombian)
     - Isabel Allende (Chilean)
   - **3 Categories**:
     - Novela
     - Realismo Mágico
     - Literatura Latinoamericana
   - **2 Publishers**:
     - Editorial Sudamericana
     - Penguin Random House
   - **4 Books**:
     - "Cien años de soledad" by García Márquez → Categories: Novela, Realismo Mágico | Publisher: Sudamericana (Ed. 1, 1967)
     - "El amor en los tiempos del cólera" by García Márquez → Categories: Novela | Publisher: Penguin (Ed. 1, 1985)
     - "La casa de los espíritus" by Allende → Categories: Novela, Realismo Mágico, Literatura Latinoamericana | Publisher: Sudamericana (Ed. 1, 1982)
     - "De amor y de sombra" by Allende → Categories: Literatura Latinoamericana | Publisher: Penguin (Ed. 1, 1984)

5. Verify at least one book has 2+ categories (Cien años de soledad and La casa de los espíritus).

Document the created records with screenshots or admin list views.