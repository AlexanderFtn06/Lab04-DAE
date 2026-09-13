from django.views.generic import ListView, DetailView
from .models import Book


class BookListView(ListView):
    model = Book
    template_name = 'library/book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.select_related('author').prefetch_related('categories', 'publications__publisher')


class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'
    context_object_name = 'book'

    def get_queryset(self):
        return Book.objects.select_related(
            'author', 'author__profile'
        ).prefetch_related(
            'categories', 'publications__publisher'
        )