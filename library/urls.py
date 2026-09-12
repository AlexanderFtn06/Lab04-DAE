from django.urls import path
from .views import BookDetailView

app_name = 'library'
urlpatterns = [
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
]