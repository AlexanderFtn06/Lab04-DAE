---
description: Create book detail template showing categories, publisher (via Publication), and author data
mode: subagent
tools:
   write: true
   edit: true
---

# Django Templates Agent

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

## Step 11: Book Detail Template

### 1. Create View in `library/views.py`
```python
from django.shortcuts import render, get_object_or_404
from .models import Book

def book_detail(request, pk):
    book = get_object_or_404(Book.objects.select_related(
        'author', 'author__profile'
    ).prefetch_related(
        'categories', 'publications__publisher'
    ), pk=pk)
    
    # Get the latest publication (most recent edition)
    latest_publication = book.publications.order_by('-publication_date').first()
    
    context = {
        'book': book,
        'latest_publication': latest_publication,
    }
    return render(request, 'library/book_detail.html', context)
```

### 2. Add URL in `library/urls.py`
```python
from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
]
```

Include in `config/urls.py`:
```python
path('library/', include('library.urls')),
```

### 3. Create Template `library/templates/library/book_detail.html`
```html
{% extends 'base.html' %}

{% block title %}{{ book.title }}{% endblock %}

{% block content %}
<div class="book-detail">
    <h1>{{ book.title }}</h1>
    
    <div class="book-meta">
        <p><strong>ISBN:</strong> {{ book.isbn }}</p>
        <p><strong>Publication Date:</strong> {{ book.publication_date }}</p>
        <p><strong>Pages:</strong> {{ book.pages }}</p>
        
        {% if book.cover %}
        <p><strong>Cover:</strong> <img src="{{ book.cover.url }}" alt="{{ book.title }} cover" style="max-width: 200px;"></p>
        {% endif %}
    </div>
    
    <div class="author-info">
        <h2>Author</h2>
        <p><strong>Name:</strong> {{ book.author.first_name }} {{ book.author.last_name }}</p>
        <p><strong>Nationality:</strong> {{ book.author.nationality }}</p>
        {% if book.author.birth_date %}
        <p><strong>Birth Date:</strong> {{ book.author.birth_date }}</p>
        {% endif %}
        
        {% if book.author.profile %}
        <div class="author-profile">
            <h3>Profile</h3>
            <p><strong>Biography:</strong> {{ book.author.profile.biography|linebreaks }}</p>
            {% if book.author.profile.website %}
            <p><strong>Website:</strong> <a href="{{ book.author.profile.website }}" target="_blank">{{ book.author.profile.website }}</a></p>
            {% endif %}
            {% if book.author.profile.twitter_handle %}
            <p><strong>Twitter:</strong> @{{ book.author.profile.twitter_handle }}</p>
            {% endif %}
        </div>
        {% endif %}
    </div>
    
    <div class="categories">
        <h2>Categories</h2>
        <ul>
        {% for category in book.categories.all %}
            <li>{{ category.name }}{% if category.description %}: {{ category.description }}{% endif %}</li>
        {% empty %}
            <li>No categories assigned</li>
        {% endfor %}
        </ul>
    </div>
    
    <div class="publisher-info">
        <h2>Publisher Information</h2>
        {% if latest_publication %}
        <p><strong>Publisher:</strong> {{ latest_publication.publisher.name }}</p>
        <p><strong>Edition:</strong> {{ latest_publication.edition }}</p>
        <p><strong>Publication Date:</strong> {{ latest_publication.publication_date }}</p>
        {% if latest_publication.publisher.website %}
        <p><strong>Publisher Website:</strong> <a href="{{ latest_publication.publisher.website }}" target="_blank">{{ latest_publication.publisher.website }}</a></p>
        {% endif %}
        {% if latest_publication.publisher.address %}
        <p><strong>Address:</strong> {{ latest_publication.publisher.address }}</p>
        {% endif %}
        
        <h3>All Editions</h3>
        <ul>
        {% for pub in book.publications.all %}
            <li>{{ pub.publisher.name }} - Edition {{ pub.edition }} ({{ pub.publication_date }})</li>
        {% endfor %}
        </ul>
        {% else %}
        <p>No publisher information available</p>
        {% endif %}
    </div>
</div>
{% endblock %}
```

### 4. Create Base Template `templates/base.html` (if not exists)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Library{% endblock %}</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }
        h1, h2, h3 { color: #333; }
        .book-detail > div { margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid #eee; }
        ul { padding-left: 1.5rem; }
    </style>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

Verify by visiting `/library/book/1/` and confirm all related data displays correctly.