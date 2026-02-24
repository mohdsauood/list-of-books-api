"""Serializers for the lists API."""

from rest_framework import serializers

from books.models import Book
from books.serializers import BookSerializer

from .models import BookList


class BookListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing BookLists.

    Returns basic list info with book IDs and count.
    Always ensures bookIds is an array (never null/undefined).
    """

    # Return array of book UUIDs - guaranteed to be array, never null
    bookIds = serializers.SerializerMethodField()
    bookCount = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        """Meta options for BookListSerializer."""

        model = BookList
        fields = ["id", "name", "description", "bookIds", "bookCount", "createdAt"]
        read_only_fields = ["id", "bookIds", "bookCount", "createdAt"]

    def get_bookIds(self, obj):
        """
        Get list of book UUIDs in this list.

        Always returns an array, even if empty (never null or undefined).
        """
        book_ids = [str(book.id) for book in obj.books.all()]
        return book_ids if book_ids else []

    def get_bookCount(self, obj):
        """Get the count of books in this list."""
        return obj.books.count()


class BookListDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed BookList view.

    Returns full book details instead of just IDs.
    """

    books = BookSerializer(many=True, read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        """Meta options for BookListDetailSerializer."""

        model = BookList
        fields = ["id", "name", "description", "books", "createdAt"]
        read_only_fields = ["id", "books", "createdAt"]


class BookListCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new BookList.

    Accepts bookIds to add books during creation.
    """

    bookIds = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        default=list,
        write_only=True,
    )

    class Meta:
        """Meta options for BookListCreateSerializer."""

        model = BookList
        fields = ["name", "description", "bookIds"]

    def create(self, validated_data):
        """Create a new book list with optional books."""
        book_ids = validated_data.pop("bookIds", [])
        book_list = BookList.objects.create(**validated_data)

        # Add books to the list
        if book_ids:
            books = Book.objects.filter(id__in=book_ids)
            book_list.books.set(books)

        return book_list

    def to_representation(self, instance):
        """Return the created list with bookIds."""
        return BookListSerializer(instance).data


class BookListUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating BookList name, description, and books.

    Accepts bookIds to replace all books in the list.
    """

    bookIds = serializers.ListField(
        child=serializers.UUIDField(),
        required=False,
        write_only=True,
    )

    class Meta:
        """Meta options for BookListUpdateSerializer."""

        model = BookList
        fields = ["name", "description", "bookIds"]

    def validate_bookIds(self, value):
        """Validate that all book IDs exist."""
        if value is not None:
            existing_books = Book.objects.filter(id__in=value)
            if len(existing_books) != len(value):
                raise serializers.ValidationError("One or more book IDs not found")
        return value

    def update(self, instance, validated_data):
        """Update list and optionally replace books."""
        book_ids = validated_data.pop("bookIds", None)

        # Update name and description
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Replace books if bookIds provided
        if book_ids is not None:
            books = Book.objects.filter(id__in=book_ids)
            instance.books.set(books)

        return instance

    def to_representation(self, instance):
        """Return the updated list with bookIds."""
        return BookListSerializer(instance).data


class AddBookToListSerializer(serializers.Serializer):
    """Serializer for adding a book to a list."""

    bookId = serializers.UUIDField()

    def validate_bookId(self, value):
        """Validate that the book exists."""
        if not Book.objects.filter(id=value).exists():
            raise serializers.ValidationError("Book not found.")
        return value
