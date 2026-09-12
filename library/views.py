from django.views.generic import DetailView
from .models import Book


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