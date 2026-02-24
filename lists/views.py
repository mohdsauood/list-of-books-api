"""Views for the lists API."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Book

from .models import BookList
from .serializers import (
    AddBookToListSerializer,
    BookListCreateSerializer,
    BookListDetailSerializer,
    BookListSerializer,
    BookListUpdateSerializer,
)


class BookListListView(APIView):
    """
    API view for listing and creating book lists.

    GET: Returns all book lists
    POST: Creates a new book list
    """

    def get(self, request):
        """
        Get all book lists.

        Returns:
            List of all book lists with bookIds and bookCount.
        """
        lists = BookList.objects.all()
        serializer = BookListSerializer(lists, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new book list.

        Request Body:
            name: List name
            description: Optional description
            bookIds: Optional list of book UUIDs to add

        Returns:
            Created list with id, name, description, bookIds
        """
        serializer = BookListCreateSerializer(data=request.data)
        if serializer.is_valid():
            book_list = serializer.save()
            return Response(
                BookListSerializer(book_list).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListDetailView(APIView):
    """
    API view for retrieving, updating, and deleting a single book list.

    GET: Returns a single book list with full book details
    PUT: Updates list name and description
    DELETE: Deletes list and cleans up orphaned books
    """

    def get_object(self, pk):
        """Get a book list by primary key."""
        try:
            return BookList.objects.get(pk=pk)
        except BookList.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Get a single book list with full book details.

        Returns:
            Book list with full book objects or 404 if not found.
        """
        book_list = self.get_object(pk)
        if book_list is None:
            return Response(
                {"error": "Book list not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = BookListDetailSerializer(book_list)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a book list's name and description.

        Request Body:
            name: New list name
            description: New description

        Returns:
            Updated list with bookIds
        """
        book_list = self.get_object(pk)
        if book_list is None:
            return Response(
                {"error": "Book list not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BookListUpdateSerializer(book_list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a book list and clean up orphaned books.

        Orphaned books are non-default books that are not in any other lists.

        Returns:
            204 No Content on success
        """
        book_list = self.get_object(pk)
        if book_list is None:
            return Response(
                {"error": "Book list not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Get books in this list before deletion
        books_in_list = list(book_list.books.all())

        # Delete the list
        book_list.delete()

        # Clean up orphaned books (not in any other lists)
        for book in books_in_list:
            if not book.book_lists.exists():
                book.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class BookListBooksView(APIView):
    """
    API view for adding books to a list.

    POST: Add a book to the list
    """

    def get_list(self, pk):
        """Get a book list by primary key."""
        try:
            return BookList.objects.get(pk=pk)
        except BookList.DoesNotExist:
            return None

    def post(self, request, pk):
        """
        Add a book to a list.

        Request Body:
            bookId: UUID of the book to add

        Returns:
            Success message or error if book already in list
        """
        book_list = self.get_list(pk)
        if book_list is None:
            return Response(
                {"error": "Book list not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AddBookToListSerializer(data=request.data)
        if serializer.is_valid():
            book_id = serializer.validated_data["bookId"]
            book = Book.objects.get(id=book_id)

            # Check if book is already in the list
            if book_list.books.filter(id=book_id).exists():
                return Response(
                    {"error": "Book is already in this list"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            book_list.books.add(book)
            return Response(
                {"message": "Book added"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListBookDetailView(APIView):
    """
    API view for removing a book from a list.

    DELETE: Remove a book from the list
    """

    def get_list(self, pk):
        """Get a book list by primary key."""
        try:
            return BookList.objects.get(pk=pk)
        except BookList.DoesNotExist:
            return None

    def delete(self, request, pk, book_id):
        """
        Remove a book from a list.

        Returns:
            Success message or 404 if list/book not found
        """
        book_list = self.get_list(pk)
        if book_list is None:
            return Response(
                {"error": "Book list not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if book is in the list
        if not book_list.books.filter(id=book_id).exists():
            return Response(
                {"error": "Book not found in this list"},
                status=status.HTTP_404_NOT_FOUND,
            )

        book_list.books.remove(book_id)
        return Response({"message": "Book removed"}, status=status.HTTP_200_OK)
