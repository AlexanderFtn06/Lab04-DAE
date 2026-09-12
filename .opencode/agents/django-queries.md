---
description: Execute Django shell queries: forward (book.author), reverse (author.books.all()), double underscore filtering; test CASCADE vs PROTECT on_delete behavior
mode: subagent
tools: bash, read
---

# Django Queries Agent

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

## Steps 9-10: Execute Queries in Django Shell

Open shell:
```bash
python manage.py shell
```

### Step 9: Forward and Reverse Queries

```python
from library.models import Author, Book, Category, Publisher, Publication

# 9.1 Forward: Book -> Author
book = Book.objects.first()
print(f"Book: {book.title}")
print(f"Author: {book.author}")  # book.author (ForeignKey)
print(f"Author full name: {book.author.first_name} {book.author.last_name}")

# 9.2 Reverse: Author -> Books (related_name='books')
author = Author.objects.first()
print(f"\nAuthor: {author}")
print(f"Books: {author.books.all()}")  # author.books.all()
for b in author.books.all():
    print(f"  - {b.title}")

# 9.3 Reverse: Author -> Profile (OneToOne related_name='profile')
print(f"\nAuthor Profile: {author.profile}")  # author.profile
print(f"Biography: {author.profile.biography}")

# 9.4 ManyToMany: Book -> Categories
book = Book.objects.get(title="Cien años de soledad")
print(f"\nBook categories: {book.categories.all()}")
for cat in book.categories.all():
    print(f"  - {cat.name}")

# 9.5 ManyToMany reverse: Category -> Books
category = Category.objects.get(name="Novela")
print(f"\nBooks in 'Novela': {category.books.all()}")
for b in category.books.all():
    print(f"  - {b.title} by {b.author}")

# 9.6 Through model: Book -> Publications -> Publisher
book = Book.objects.get(title="Cien años de soledad")
print(f"\nPublications for '{book.title}':")
for pub in book.publication_set.all():  # or book.publications if related_name
    print(f"  - {pub.publisher.name}, Ed. {pub.edition}, {pub.publication_date}")

# 9.7 Double underscore filtering
# Books by Colombian authors
colombian_books = Book.objects.filter(author__nationality="Colombian")
print(f"\nBooks by Colombian authors: {colombian_books.count()}")

# Books in 'Realismo Mágico' category
magical_books = Book.objects.filter(categories__name="Realismo Mágico")
print(f"Books in Realismo Mágico: {magical_books.count()}")

# Books published by Sudamericana
sudamericana_books = Book.objects.filter(publications__publisher__name="Editorial Sudamericana")
print(f"Books by Sudamericana: {sudamericana_books.count()}")

# Authors with more than 1 book
from django.db.models import Count
prolific_authors = Author.objects.annotate(num_books=Count('books')).filter(num_books__gt=1)
print(f"\nAuthors with >1 book: {[str(a) for a in prolific_authors]}")
```

### Step 10: Test on_delete Behavior

**Test 1: CASCADE (current default)**
```python
# Delete author with books - CASCADE deletes books too
author = Author.objects.get(last_name="García Márquez")
print(f"Books before delete: {Book.objects.count()}")
author.delete()
print(f"Books after delete: {Book.objects.count()}")
# Result: Books by this author are DELETED
```

**Test 2: Change to PROTECT and compare**
1. Modify `Book.author` field: `on_delete=models.PROTECT`
2. Generate and apply migration:
   ```bash
   python manage.py makemigrations library
   python manage.py migrate
   ```
3. Test again:
   ```python
   author = Author.objects.get(last_name="Allende")
   try:
       author.delete()
   except Exception as e:
       print(f"Error: {e}")
   # Result: ProtectedError raised, author NOT deleted, books preserved
   ```

Document both behaviors with output screenshots.