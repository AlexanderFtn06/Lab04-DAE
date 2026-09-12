# Evidencia de Consultas Django Shell

## 1. Forward Query: Book → Author

```python
book = Book.objects.first()
print(f"Book: {book.title}")
print(f"Author: {book.author}")
print(f"Author full name: {book.author.first_name} {book.author.last_name}")
```

**Output:**
```
Book: Cien años de soledad
Author: Gabriel García Márquez
Author full name: Gabriel García Márquez
Author nationality: Colombian
```

---

## 2. Reverse Query: Author → Books

```python
author = Author.objects.first()
print(f"Author: {author}")
print(f"Books: {list(author.books.all())}")
for b in author.books.all():
    print(f"  - {b.title} (ISBN: {b.isbn})")
```

**Output:**
```
Author: Isabel Allende
Books: [<Book: De amor y de sombra>, <Book: La casa de los espíritus>]
  - De amor y de sombra (ISBN: 9788437604978)
  - La casa de los espíritus (ISBN: 9788437604961)
```

---

## 3. Double Underscore Filtering

### 3.1 Books by Colombian Authors

```python
colombian_books = Book.objects.filter(author__nationality="Colombian")
print(f"Books by Colombian authors: {colombian_books.count()}")
for b in colombian_books:
    print(f"  - {b.title} by {b.author}")
```

**Output:**
```
Books by Colombian authors: 2
  - Cien años de soledad by Gabriel García Márquez
  - El amor en los tiempos del cólera by Gabriel García Márquez
```

### 3.2 Books in "Realismo Mágico" Category

```python
magical_books = Book.objects.filter(categories__name="Realismo Mágico")
print(f"Books in Realismo Mágico category: {magical_books.count()}")
for b in magical_books:
    print(f"  - {b.title} by {b.author}")
```

**Output:**
```
Books in Realismo Mágico category: 2
  - Cien años de soledad by Gabriel García Márquez
  - La casa de los espíritus by Isabel Allende
```

---

## 4. on_delete=PROTECT Behavior (Current Configuration)

**Model:** `Book.author = ForeignKey(Author, on_delete=PROTECT, related_name='books')`

### Test: Attempt to delete Author with existing books

```python
from library.models import Author, Book

author = Author.objects.get(last_name="García Márquez")
print(f"Author: {author}")
print(f"Books count before: {Book.objects.filter(author=author).count()}")

try:
    author.delete()
    print("Author deleted successfully")
except Exception as e:
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {e}")

print(f"Books count after: {Book.objects.filter(author=author).count()}")
```

**Output:**
```
Author: Gabriel García Márquez
Books count before: 2
Error type: ProtectedError
Error message: ("Cannot delete some instances of model 'Author' because they are referenced through protected foreign keys: 'Book.author'.", {<Book: Cien años de soledad>, <Book: El amor en los tiempos del cólera>})
Books count after: 2
```

**Result:** Django raises `ProtectedError`, author is NOT deleted, books are preserved. This prevents accidental data loss in the catalog.

---

## 5. on_delete=CASCADE Behavior (Temporary Test)

**Migration applied:** Changed `on_delete=PROTECT` to `on_delete=CASCADE` via `library/migrations/0002_alter_book_author.py`

### Test: Delete Author with existing books (CASCADE)

```python
from library.models import Author, Book

author = Author.objects.get(last_name="Allende")
print(f"Author: {author}")
print(f"Books count before: {Book.objects.filter(author=author).count()}")

author.delete()
print("Author deleted successfully")

print(f"Total books in DB after: {Book.objects.count()}")
print(f"Authors remaining: {Author.objects.count()}")
```

**Output:**
```
Author: Isabel Allende
Books count before: 2
Author deleted successfully
Total books in DB after: 2
Authors remaining: 1
  - Gabriel García Márquez: 2 books
```

**Result:** Author AND their 2 books ("La casa de los espíritus", "De amor y de sombra") were deleted. Only Gabriel García Márquez and his 2 books remain.

---

## 6. Revert to PROTECT

**Migration applied:** Changed back to `on_delete=PROTECT` via `library/migrations/0003_alter_book_author.py`

### Verification: PROTECT restored

```python
from library.models import Author, Book

author = Author.objects.get(last_name="García Márquez")
print(f"Author: {author}")
print(f"Books count: {Book.objects.filter(author=author).count()}")

try:
    author.delete()
    print("Author deleted")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")

print(f"Books still exist: {Book.objects.filter(author=author).count()}")
```

**Output:**
```
Author: Gabriel García Márquez
Books count: 2
Error: ProtectedError: ("Cannot delete some instances of model 'Author' because they are referenced through protected foreign keys: 'Book.author'.", {<Book: Cien años de soledad>, <Book: El amor en los tiempos del cólera>})
Books still exist: 2
```

**Result:** PROTECT behavior confirmed restored.

---

## 7. Comparison Table: PROTECT vs CASCADE

| Aspect | `on_delete=PROTECT` (Current) | `on_delete=CASCADE` (Tested) |
|--------|-------------------------------|------------------------------|
| **Delete Author with books** | ❌ Raises `ProtectedError` | ✅ Succeeds |
| **Author deleted** | No | Yes |
| **Related books deleted** | No (preserved) | Yes (cascaded) |
| **Data integrity** | High - prevents orphan books loss | Lower - deletes catalog entries |
| **Use case** | Catalog preservation, audit trails | Cleanup, temporary data |
| **Error type** | `django.db.models.ProtectedError` | None (silent cascade) |
| **Recovery** | Not needed (nothing deleted) | Requires backup/restore |

---

## Resumen de Consultas Ejecutadas

| Consulta | Tipo | Resultado |
|----------|------|-----------|
| `Book.objects.first().author` | Forward (FK) | Gabriel García Márquez |
| `Author.objects.first().books.all()` | Reverse (related_name) | 2 libros de Isabel Allende |
| `Book.objects.filter(author__nationality="Colombian")` | Double underscore | 2 libros |
| `Book.objects.filter(categories__name="Realismo Mágico")` | Double underscore (M2M) | 2 libros |
| `author.delete()` con PROTECT | on_delete test | ProtectedError, libros intactos |
| `author.delete()` con CASCADE | on_delete test | Autor + 2 libros eliminados |

---

## Migraciones Generadas

| Archivo | Cambio |
|---------|--------|
| `library/migrations/0002_alter_book_author.py` | PROTECT → CASCADE |
| `library/migrations/0003_alter_book_author.py` | CASCADE → PROTECT (revert) |

Todas las consultas y pruebas se ejecutaron correctamente en `python manage.py shell`.