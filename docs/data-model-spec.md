# Data Model Specification - Lab 4: Relación de Modelos en Django

**Única fuente de verdad para todos los sub-agentes. No modificar nombres de campos sin consultar.**

---

## Author

| Campo | Tipo | Opciones |
|-------|------|----------|
| first_name | CharField | max_length=100 |
| last_name | CharField | max_length=100 |
| birth_date | DateField | null=True, blank=True |
| nationality | CharField | max_length=100, blank=True |

**Meta:**
- ordering = ['last_name', 'first_name']

**__str__:**
- `f"{self.first_name} {self.last_name}"`

---

## AuthorProfile

Relación: **OneToOneField → Author**

| Campo | Tipo | Opciones |
|-------|------|----------|
| author | OneToOneField | Author, on_delete=CASCADE, related_name='profile' |
| biography | TextField | blank=True |
| photo | ImageField | upload_to='authors/', blank=True, null=True |
| website | URLField | blank=True |

---

## Publisher

| Campo | Tipo | Opciones |
|-------|------|----------|
| name | CharField | max_length=200 |
| country | CharField | max_length=100 |
| founded_year | PositiveIntegerField | null=True, blank=True |

---

## Category

| Campo | Tipo | Opciones |
|-------|------|----------|
| name | CharField | max_length=100, unique=True |
| description | TextField | blank=True |

**Meta:**
- verbose_name_plural = "Categories"
- ordering = ['name']

**__str__:**
- `self.name`

---

## Book

| Campo | Tipo | Opciones |
|-------|------|----------|
| title | CharField | max_length=200 |
| isbn | CharField | max_length=13, unique=True |
| publication_year | PositiveIntegerField | |
| summary | TextField | blank=True |
| cover | ImageField | upload_to='books/', blank=True, null=True |

### Relaciones

| Relación | Tipo | Configuración | Justificación |
|----------|------|---------------|---------------|
| author | ForeignKey | Author, on_delete=PROTECT, related_name='books' | Un libro no debe quedar huérfano ni el autor debe arrastrar el borrado de sus libros; se protege la integridad del catálogo. |
| categories | ManyToManyField | Category, related_name='books', blank=True | Un libro puede tener múltiples categorías; una categoría aplica a muchos libros. |
| publishers | ManyToManyField | Publisher, through='Publication', related_name='books' | Un libro puede publicarse en múltiples editoriales (distintas ediciones) y una editorial publica muchos libros. Requiere datos extra (fecha, edición) → modelo intermedio. |

**Meta:**
- ordering = ['title']

**__str__:**
- `self.title`

---

## Publication (Modelo Intermedio / Through)

Relación: **Through de Book ↔ Publisher**

| Campo | Tipo | Opciones |
|-------|------|----------|
| book | ForeignKey | Book, on_delete=CASCADE |
| publisher | ForeignKey | Publisher, on_delete=CASCADE |
| publication_date | DateField | |
| edition | PositiveIntegerField | default=1 |

**Meta:**
- unique_together = ['book', 'publisher', 'edition']
- ordering = ['-publication_date']

**__str__:**
- `f"{self.book.title} - {self.publisher.name} (Ed. {self.edition})"`

---

## Resumen de Tablas Esperadas (post-migración)

| Tabla | Descripción |
|-------|-------------|
| library_author | Autores |
| library_authorprofile | Perfiles de autor (1:1) |
| library_publisher | Editoriales |
| library_category | Categorías |
| library_book | Libros |
| library_book_categories | M2M automático Book-Category |
| library_publication | M2M con datos extra Book-Publisher (through) |

---

## Reglas de Negocio Clave

1. **on_delete=PROTECT en Book.author**: Impide borrar un autor si tiene libros. Evita pérdida de datos del catálogo.
2. **related_name='books' en Author → Book**: Permite `author.books.all()`.
3. **related_name='profile' en AuthorProfile → Author**: Permite `author.profile`.
4. **related_name='books' en Category y Publisher**: Permite `category.books.all()` y `publisher.books.all()`.
5. **unique_together en Publication**: Evita duplicados de misma edición de un libro en una editorial.
6. **upload_to en ImageFields**: 'authors/' para AuthorProfile.photo, 'books/' para Book.cover.

---

## Datos de Prueba (Paso 8 - Admin)

### Authors (2)
1. Gabriel García Márquez, Colombian, birth_date=1927-03-06
2. Isabel Allende, Chilean, birth_date=1942-08-02

### Categories (3)
1. Novela
2. Realismo Mágico
3. Literatura Latinoamericana

### Publishers (2)
1. Editorial Sudamericana, Argentina, 1939
2. Penguin Random House, USA, 2013

### Books (4)
1. "Cien años de soledad", ISBN=9788437604947, 1967, author=García Márquez, categories=[Novela, Realismo Mágico], publications=[Sudamericana, 1967-05-30, Ed.1]
2. "El amor en los tiempos del cólera", ISBN=9788437604954, 1985, author=García Márquez, categories=[Novela], publications=[Penguin, 1985-01-01, Ed.1]
3. "La casa de los espíritus", ISBN=9788437604961, 1982, author=Allende, categories=[Novela, Realismo Mágico, Literatura Latinoamericana], publications=[Sudamericana, 1982-10-01, Ed.1]
4. "De amor y de sombra", ISBN=9788437604978, 1984, author=Allende, categories=[Literatura Latinoamericana], publications=[Penguin, 1984-01-01, Ed.1]

---

## Consultas de Validación (Paso 9-10)

```python
# Forward
book.author                    # Author
book.categories.all()          # QuerySet[Category]
book.publications.all()        # QuerySet[Publication]

# Reverse
author.books.all()             # QuerySet[Book]
author.profile                 # AuthorProfile
category.books.all()           # QuerySet[Book]
publisher.books.all()          # QuerySet[Book] (via through)

# Double underscore
Book.objects.filter(author__nationality='Colombian')
Book.objects.filter(categories__name='Realismo Mágico')
Book.objects.filter(publications__publisher__name='Editorial Sudamericana')

# on_delete test
# CASCADE: author.delete() → borra libros
# PROTECT: author.delete() → ProtectedError
```

---

**Última actualización:** 2026-09-12
**Versión:** 1.0