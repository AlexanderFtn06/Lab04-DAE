from django.contrib import admin
from .models import Author, Book, Publisher, Category, AuthorProfile, Publication


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'nationality']
    search_fields = ['first_name', 'last_name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'publication_year']
    list_filter = ['author', 'categories']
    filter_horizontal = ['categories']
    search_fields = ['title', 'isbn']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'founded_year']
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