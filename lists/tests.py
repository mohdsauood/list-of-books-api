"""Tests for the lists API."""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book

from .models import BookList


class BookListModelTest(TestCase):
    """Test cases for the BookList model."""

    def test_booklist_creation(self):
        """Test creating a book list."""
        book_list = BookList.objects.create(
            name="Test List",
            description="Test description",
        )
        self.assertEqual(book_list.name, "Test List")
        self.assertEqual(book_list.description, "Test description")

    def test_booklist_string_representation(self):
        """Test book list string representation."""
        book_list = BookList.objects.create(name="Test List")
        self.assertEqual(str(book_list), "Test List")


class BookListAPITest(APITestCase):
    """Test cases for the BookLists API."""

    def setUp(self):
        """Set up test data."""
        # Create test books
        self.book1 = Book.objects.create(
            title="Book 1",
            author="Author 1",
            year=2020,
        )
        self.book2 = Book.objects.create(
            title="Book 2",
            author="Author 2",
            year=2021,
        )
        self.book3 = Book.objects.create(
            title="Book 3",
            author="Author 3",
            year=2019,
        )

        # Create a test list
        self.test_list = BookList.objects.create(
            name="Test List",
            description="Test description",
        )
        self.test_list.books.add(self.book1)

    def test_get_all_lists(self):
        """Test getting all book lists."""
        url = reverse("booklist-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test List")
        self.assertEqual(len(response.data[0]["bookIds"]), 1)

    def test_create_empty_list(self):
        """Test creating an empty book list."""
        url = reverse("booklist-list")
        data = {
            "name": "New List",
            "description": "New description",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New List")
        self.assertEqual(len(response.data["bookIds"]), 0)

    def test_create_list_with_books(self):
        """Test creating a list with books."""
        url = reverse("booklist-list")
        data = {
            "name": "List with Books",
            "description": "Description",
            "bookIds": [str(self.book1.id), str(self.book2.id)],
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data["bookIds"]), 2)

    def test_get_list_detail(self):
        """Test getting detailed list with books."""
        url = reverse("booklist-detail", kwargs={"pk": self.test_list.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test List")
        self.assertEqual(len(response.data["books"]), 1)
        self.assertEqual(response.data["books"][0]["title"], "Book 1")

    def test_update_list(self):
        """Test updating a list's name and description."""
        url = reverse("booklist-detail", kwargs={"pk": self.test_list.pk})
        data = {
            "name": "Updated List",
            "description": "Updated description",
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated List")

    def test_add_book_to_list(self):
        """Test adding a book to a list."""
        url = reverse("booklist-books", kwargs={"pk": self.test_list.pk})
        data = {"bookId": str(self.book2.id)}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Book added")

        # Verify book was added
        self.test_list.refresh_from_db()
        self.assertEqual(self.test_list.books.count(), 2)

    def test_add_duplicate_book_to_list(self):
        """Test adding a book that's already in the list."""
        url = reverse("booklist-books", kwargs={"pk": self.test_list.pk})
        data = {"bookId": str(self.book1.id)}  # book1 is already in the list
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_book_from_list(self):
        """Test removing a book from a list."""
        url = reverse("booklist-book-detail", kwargs={"pk": self.test_list.pk, "book_id": self.book1.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Book removed")

        # Verify book was removed
        self.test_list.refresh_from_db()
        self.assertEqual(self.test_list.books.count(), 0)

    def test_delete_list_with_orphaned_books(self):
        """Test deleting a list and cleaning up orphaned books."""
        # Add a non-default book to the list
        self.test_list.books.add(self.book2)
        book2_id = self.book2.id

        url = reverse("booklist-detail", kwargs={"pk": self.test_list.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # List should be deleted
        self.assertFalse(BookList.objects.filter(pk=self.test_list.pk).exists())

        # Orphaned books should be deleted
        self.assertFalse(Book.objects.filter(pk=book2_id).exists())
