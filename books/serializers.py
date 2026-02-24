"""Serializers for the books API."""

from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    Converts Book model instances to JSON and vice versa.
    Uses camelCase for frontend compatibility.
    """

    # Map Python snake_case to JavaScript camelCase
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        """Meta options for BookSerializer."""

        model = Book
        fields = ["id", "title", "author", "year", "createdAt"]
        read_only_fields = ["id", "createdAt"]


class BookCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new Book.

    Only accepts title, author, and year.
    """

    class Meta:
        """Meta options for BookCreateSerializer."""

        model = Book
        fields = ["title", "author", "year"]
