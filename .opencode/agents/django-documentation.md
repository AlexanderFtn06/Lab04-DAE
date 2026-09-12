---
description: Write deliverable evidence section with course format: student name, title, result screenshot, code, result explanation, test cases, and project structure screenshot
mode: subagent
tools:
  write: true
  edit: true
---

# Django Documentation Agent

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

## Deliverable Evidence Document

Create `ENTREGABLE.md` (or `evidencia.md`) with this structure:

---

# Evidencia de Entregable - Laboratorio 4: Relación de Modelos en Django

## 1. Datos del Alumno
- **Nombre:** [Tu Nombre Completo]
- **Curso:** Desarrollo de Aplicaciones Empresariales
- **Semana:** 4
- **Fecha:** [Fecha de entrega]
- **Repositorio:** [URL del repositorio GitHub del equipo]

## 2. Título del Desarrollo
**Implementación de relaciones entre modelos en Django: ForeignKey, OneToOneField, ManyToManyField y modelo intermedio con `through`**

## 3. Captura del Resultado
![Resultado de la aplicación](capturas/resultado_app.png)
*Descripción: Vista de detalle de libro mostrando autor, categorías, editorial y perfil del autor.*

## 4. Código Implementado

### 4.1 Modelos (`library/models.py`)
```python
# [Pegar aquí el contenido completo de models.py]
```

### 4.2 Admin (`library/admin.py`)
```python
# [Pegar aquí el contenido completo de admin.py]
```

### 4.3 Vista y URL (`library/views.py`, `library/urls.py`)
```python
# [Pegar aquí el contenido relevante]
```

### 4.4 Plantilla (`library/templates/library/book_detail.html`)
```html
<!-- [Pegar aquí el contenido completo] -->
```

### 4.5 Configuración de Medios (`config/settings.py`, `config/urls.py`)
```python
# [Pegar las líneas relevantes de MEDIA_URL/MEDIA_ROOT y static()]
```

## 5. Explicación del Resultado

### Relaciones Implementadas

| Relación | Tipo | Justificación |
|----------|------|---------------|
| Book → Author | ForeignKey (CASCADE) | Un libro tiene un autor; un autor tiene muchos libros. Si se borra el autor, se borran sus libros. |
| AuthorProfile → Author | OneToOneField | Cada autor tiene máximo un perfil extendido. Es una extensión 1:1. |
| Book ↔ Category | ManyToManyField | Un libro puede tener varias categorías; una categoría aplica a muchos libros. |
| Book ↔ Publisher | ManyToManyField con `through=Publication` | Un libro puede tener varias editoriales (distintas ediciones) y una editorial publica muchos libros. Se requieren datos extra: fecha de publicación y número de edición. |

### Consultas Probadas (Shell)

1. **Ida (Forward)**: `book.author` → Acceso directo al autor desde el libro.
2. **Vuelta (Reverse)**: `author.books.all()` → Todos los libros de un autor (gracias a `related_name='books'`).
3. **Filtro con `__`**: `Book.objects.filter(author__nationality='Colombian')` → Libros de autores colombianos.
4. **ManyToMany ida**: `book.categories.all()` → Categorías de un libro.
5. **ManyToMany vuelta**: `category.books.all()` → Libros en una categoría.
6. **Through model**: `book.publications.all()` → Ediciones con editorial, fecha y número.

### Comportamiento `on_delete`

| Configuración | Acción al borrar Autor | Resultado |
|---------------|------------------------|-----------|
| `CASCADE` | `author.delete()` | Se borran el autor Y sus libros automáticamente. |
| `PROTECT` | `author.delete()` | Lanza `ProtectedError`; NO se borra el autor ni los libros. |

## 6. Casos de Prueba

| Caso | Entrada | Resultado Esperado | Resultado Obtenido |
|------|---------|-------------------|-------------------|
| CP-01 | Crear autor con perfil | AuthorProfile creado y vinculado | ✅ |
| CP-02 | Asignar 2 categorías a un libro | `book.categories.count() == 2` | ✅ |
| CP-03 | Publicar libro en 2 editoriales | 2 registros en Publication | ✅ |
| CP-04 | Borrar autor con CASCADE | Libros del autor eliminados | ✅ |
| CP-05 | Borrar autor con PROTECT | Error ProtectedError, datos intactos | ✅ |
| CP-06 | Consultar libros por categoría | QuerySet con libros correctos | ✅ |
| CP-07 | Ver detalle de libro en web | Muestra autor, categorías, editorial | ✅ |

## 7. Captura de Estructura del Proyecto en el Editor

![Estructura del proyecto](capturas/estructura_proyecto.png)
*Vista del explorador de archivos en VS Code mostrando la estructura completa del proyecto Django.*

---

### Checklist Final
- [ ] Modelo Author con campos, Meta, __str__
- [ ] Modelo Book con ForeignKey a Author
- [ ] Modelo AuthorProfile con OneToOneField a Author
- [ ] Modelo Category con ManyToManyField en Book
- [ ] Modelo Publisher con Through model Publication
- [ ] Publication con publication_date y edition
- [ ] Migraciones generadas y aplicadas
- [ ] Admin configurado para todos los modelos
- [ ] Datos de prueba cargados (2 autores, 4 libros, 3 categorías, 2 editoriales)
- [ ] Consultas en shell documentadas
- [ ] Prueba on_delete CASCADE vs PROTECT
- [ ] Plantilla book_detail funcional
- [ ] Repositorio GitHub actualizado
- [ ] Documentación completa

---

**Nota**: Reemplaza `[...]` con tu información real. Guarda las capturas en carpeta `capturas/` del repositorio.