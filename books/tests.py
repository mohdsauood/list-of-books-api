"""Tests for the books API."""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Book


class BookModelTest(TestCase):
    """Test cases for the Book model."""

    def test_book_creation(self):
        """Test creating a book."""
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            year=2023,
        )
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.year, 2023)

    def test_book_string_representation(self):
        """Test book string representation."""
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            year=2023,
        )
        expected_str = "Test Book by Test Author (2023)"
        self.assertEqual(str(book), expected_str)


class BookAPITest(APITestCase):
    """Test cases for the Books API."""

    def setUp(self):
        """Set up test data."""
        # Create test books
        self.book1 = Book.objects.create(
            title="Book One",
            author="Author One",
            year=2020,
        )
        self.book2 = Book.objects.create(
            title="Book Two",
            author="Author Two",
            year=2023,
        )

    def test_get_all_books(self):
        """Test getting all books."""
        url = reverse("book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 5)

    def test_create_book(self):
        """Test creating a new book."""
        url = reverse("book-list")
        data = {
            "title": "New Book",
            "author": "New Author",
            "year": 2024,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")
        self.assertEqual(response.data["author"], "New Author")
        self.assertEqual(response.data["year"], 2024)

    def test_create_book_missing_fields(self):
        """Test creating a book with missing fields."""
        url = reverse("book-list")
        data = {"title": "Incomplete Book"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_single_book(self):
        """Test getting a single book."""
        url = reverse("book-detail", kwargs={"pk": self.book1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Book One")

    def test_get_nonexistent_book(self):
        """Test getting a book that doesn't exist."""
        url = reverse("book-detail", kwargs={"pk": "00000000-0000-0000-0000-000000000000"})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_book(self):
        """Test deleting a book."""
        url = reverse("book-detail", kwargs={"pk": self.book2.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())
