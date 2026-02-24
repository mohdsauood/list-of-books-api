"""BookList model for managing collections of books."""

import uuid

from django.db import models

from books.models import Book


class BookList(models.Model):
    """
    BookList model representing a collection of books.

    Attributes:
        id: UUID primary key for the list
        name: The name of the book list
        description: Optional description of the list
        books: Many-to-many relationship with Book model
        created_at: Timestamp when the list was created
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True, default="")
    books = models.ManyToManyField(Book, blank=True, related_name="book_lists")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for the BookList model."""

        ordering = ["-created_at"]

    def __str__(self):
        """Return string representation of the book list."""
        return self.name
