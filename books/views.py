"""Views for the books API."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book
from .serializers import BookCreateSerializer, BookSerializer


class BookListView(APIView):
    """
    API view for listing and creating books.

    GET: Returns all books
    POST: Creates a new book
    """

    def get(self, request):
        """
        Get all books.

        Returns:
            List of all books with their details.
        """
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new book.

        Request Body:
            title: Book title
            author: Author name
            year: Publication year

        Returns:
            Created book with id and isDefault=False
        """
        serializer = BookCreateSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            return Response(
                BookSerializer(book).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    """
    API view for retrieving and deleting a single book.

    GET: Returns a single book
    DELETE: Deletes a book (if allowed)
    """

    def get_object(self, pk):
        """Get a book by primary key."""
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Get a single book by ID.

        Returns:
            Book details or 404 if not found.
        """
        book = self.get_object(pk)
        if book is None:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def delete(self, request, pk):
        """
        Delete a book.

        Rules:
            - Cannot delete books that are in any lists

        Returns:
            204 No Content on success
            400 Bad Request if deletion not allowed
        """
        book = self.get_object(pk)
        if book is None:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if book is in any lists
        if book.book_lists.exists():
            return Response(
                {"error": "Cannot delete book that is in a list"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
