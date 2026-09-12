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

## Resumen de Consultas Ejecutadas

| Consulta | Tipo | Resultado |
|----------|------|-----------|
| `Book.objects.first().author` | Forward (FK) | Gabriel García Márquez |
| `Author.objects.first().books.all()` | Reverse (related_name) | 2 libros de Isabel Allende |
| `Book.objects.filter(author__nationality="Colombian")` | Double underscore | 2 libros |
| `Book.objects.filter(categories__name="Realismo Mágico")` | Double underscore (M2M) | 2 libros |

Todas las consultas se ejecutaron correctamente en `python manage.py shell`.