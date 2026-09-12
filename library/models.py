from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    founded_year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class AuthorProfile(models.Model):
    author = models.OneToOneField(
        Author,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    biography = models.TextField(blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"Perfil de {self.author}"


class Publication(models.Model):
    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE
    )
    publication_date = models.DateField()
    edition = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['book', 'publisher', 'edition']
        ordering = ['-publication_date']

    def __str__(self):
        return f"{self.book.title} - {self.publisher.name} (Ed. {self.edition})"


class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    publication_year = models.PositiveIntegerField()
    summary = models.TextField(blank=True)
    cover = models.ImageField(upload_to='books/', blank=True, null=True)
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name='books'
    )
    categories = models.ManyToManyField(
        Category,
        related_name='books',
        blank=True
    )
    publishers = models.ManyToManyField(
        Publisher,
        through='Publication',
        related_name='books'
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title