---
description: Push project to team GitHub repository (single repo per team)
mode: subagent
tools:
   write: true
---

# Django Git Agent

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

## Step 12: Push to Team Repository

### 1. Initialize Git (if not already)
```bash
git init
```

### 2. Create .gitignore
```bash
cat > .gitignore << 'EOF'
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Environment
.env
.venv
venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF
```

### 3. Add and Commit
```bash
git add .
git commit -m "feat: initial Django project with library app models and relationships

- Author, Book, Publisher, Category, AuthorProfile, Publication models
- ForeignKey: Book -> Author (CASCADE)
- OneToOneField: AuthorProfile -> Author
- ManyToManyField: Book <-> Category
- Through model: Publication (Book <-> Publisher with date and edition)
- Admin configuration for all models
- Book detail template with related data
- Media file configuration"
```

### 4. Create GitHub Repository (via web or CLI)
- Go to GitHub.com → New Repository
- Name: `dae-lab04-relacion-modelos` (or team's naming convention)
- Visibility: Private (for class) or Public
- Do NOT initialize with README, .gitignore, or license

### 5. Add Remote and Push
```bash
git remote add origin https://github.com/<team-org>/<repo-name>.git
git branch -M main
git push -u origin main
```

### 6. Verify
- Check GitHub repo shows all files
- Verify `.gitignore` excludes `db.sqlite3`, `media/`, `__pycache__/`
- Confirm no credentials in `settings.py` (use environment variables)

### Team Notes
- Only ONE repository per team
- All team members should have push access
- Use feature branches for future work: `git checkout -b feature/new-feature`
- Create PRs for review before merging to main