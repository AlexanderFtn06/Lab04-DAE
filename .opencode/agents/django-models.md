---
description: Declare Author, Book, Publisher, Category models with fields, Meta and __str__; link Book-Author (ForeignKey), Author-AuthorProfile (OneToOne), Book-Category (ManyToMany), Book-Publisher through Publication (with date and edition)
mode: subagent
tools: write, edit, bash
---

# Django Models Agent

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

## Steps 3-6: Declare Models and Relationships

### Step 3: Author Model
```python
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
```

### Step 4: Book-Author Relationship (ForeignKey)
**Justification**: A book has ONE author, but an author can have MANY books. This is a classic one-to-many relationship. ForeignKey goes on the "many" side (Book). Use `on_delete=models.CASCADE` (if author deleted, their books are deleted) or `PROTECT` (prevent author deletion if they have books). Use `related_name='books'` for reverse access.

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    pages = models.PositiveIntegerField()
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title
```

### Step 5: AuthorProfile (OneToOneField)
**Justification**: Each author has at most ONE profile with additional info. OneToOneField creates a one-to-one link. Goes on either side; typically on the "extension" model.

```python
class AuthorProfile(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE, related_name='profile')
    biography = models.TextField(blank=True)
    website = models.URLField(blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"Profile of {self.author}"
```

### Step 6: Category and Publisher with Through Model
**Justification for ManyToMany (Book-Category)**: A book can belong to MULTIPLE categories, and a category can have MULTIPLE books. This is a many-to-many relationship.

**Justification for Through Model (Book-Publisher)**: A book can be published by MULTIPLE publishers (different editions), and a publisher publishes MANY books. We need to store EXTRA DATA per relationship: publication date and edition number. This requires an explicit intermediate model with `through`.

```python
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    founded_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Publication(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.DateField()
    edition = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ['book', 'publisher', 'edition']
        ordering = ['-publication_date']
    
    def __str__(self):
        return f"{self.book.title} - {self.publisher.name} (Ed. {self.edition})"


# Add to Book model:
categories = models.ManyToManyField(Category, related_name='books', blank=True)
publishers = models.ManyToManyField(Publisher, through=Publication, related_name='books')
```

Before each relationship, explain WHY it's that type and not another. Check existing models.py first.