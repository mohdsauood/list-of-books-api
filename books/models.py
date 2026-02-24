"""Book model for the books API."""

import uuid

from django.db import models


class Book(models.Model):
    """
    Book model representing a single book in the system.

    Attributes:
        id: UUID primary key for the book
        title: The title of the book
        author: The author's name
        year: Year the book was published
        created_at: Timestamp when the book was created
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=False)
    author = models.CharField(max_length=255, blank=False)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for the Book model."""

        ordering = ["title"]

    def __str__(self):
        """Return string representation of the book."""
        return f"{self.title} by {self.author} ({self.year})"
