"""URL configuration for the lists app."""

from django.urls import path

from .views import (
    BookListBookDetailView,
    BookListBooksView,
    BookListDetailView,
    BookListListView,
)

urlpatterns = [
    path("", BookListListView.as_view(), name="booklist-list"),
    path("<uuid:pk>/", BookListDetailView.as_view(), name="booklist-detail"),
    path("<uuid:pk>/books/", BookListBooksView.as_view(), name="booklist-books"),
    path(
        "<uuid:pk>/books/<uuid:book_id>/",
        BookListBookDetailView.as_view(),
        name="booklist-book-detail",
    ),
]
