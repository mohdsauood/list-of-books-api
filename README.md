# Book List Management API

A Django REST API for managing books and book lists. Built with Django REST Framework, featuring automatic data loading and Docker support.

## 🚀 Quick Start

### Option 1: Run Locally

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations (automatically loads initial books)
python manage.py migrate

# 4. Start server
python manage.py runserver
```

**API available at:** `http://localhost:8000/`

### Option 2: Run with Docker

```bash
# 1. Build Docker image
docker build -t books-api .

# 2. Run container
docker run -p 8000:8000 books-api
```

**API available at:** `http://localhost:8000/`

Both methods automatically load 5 initial books (Dune, 1984, Ender's Game, etc.) - no manual setup required! 🎉

## 📚 API Documentation

### Books Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/api/books/` | Get all books | - | `[{id, title, author, year, createdAt}]` |
| POST | `/api/books/` | Create new book | `{title, author, year}` | `{id, title, author, year, createdAt}` |
| GET | `/api/books/{id}/` | Get single book | - | `{id, title, author, year, createdAt}` |
| DELETE | `/api/books/{id}/` | Delete book | - | `204 No Content` |

### Book Lists Endpoints

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/api/lists/` | Get all book lists | - | `[{id, name, description, bookIds: [], bookCount, createdAt}]` |
| POST | `/api/lists/` | Create book list | `{name, description, bookIds?: []}` | `{id, name, description, bookIds: [], bookCount, createdAt}` |
| GET | `/api/lists/{id}/` | Get list with full books | - | `{id, name, description, books: [{...}], createdAt}` |
| PUT | `/api/lists/{id}/` | Update list | `{name, description, bookIds?: []}` | `{id, name, description, bookIds: [], bookCount, createdAt}` |
| DELETE | `/api/lists/{id}/` | Delete list | - | `204 No Content` |

### List-Book Management

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/api/lists/{id}/books/` | Add book to list | `{bookId}` | `{message: "Book added"}` |
| DELETE | `/api/lists/{id}/books/{bookId}/` | Remove book from list | - | `{message: "Book removed"}` |

## 📋 Data Models

### Book Model
```json
{
  "id": "uuid-string",
  "title": "Book Title",
  "author": "Author Name", 
  "year": 1999,
  "createdAt": "2026-01-01T00:00:00Z"
}
```

### Book List Model
```json
{
  "id": "uuid-string",
  "name": "My Reading List",
  "description": "Books I want to read",
  "bookIds": ["book-uuid-1", "book-uuid-2"],
  "bookCount": 2,
  "createdAt": "2026-01-01T00:00:00Z"
}
```

**List Detail View** includes full book objects:
```json
{
  "id": "uuid-string",
  "name": "My Reading List", 
  "description": "Books I want to read",
  "books": [
    {"id": "book-uuid-1", "title": "Dune", "author": "Frank Herbert", "year": 1965},
    {"id": "book-uuid-2", "title": "1984", "author": "George Orwell", "year": 1949}
  ],
  "createdAt": "2026-01-01T00:00:00Z"
}
```

## 📁 Project Structure

```
books_api/
├── books/                    # Books app
│   ├── fixtures/            # Initial book data
│   │   └── initial_books.json
│   ├── management/          # Auto-load commands
│   │   └── commands/
│   ├── models.py            # Book model
│   ├── serializers.py       # Book serializers  
│   ├── views.py             # Book API views
│   └── urls.py              # Book URL patterns
├── lists/                   # Book lists app
│   ├── models.py            # BookList model
│   ├── serializers.py       # BookList serializers
│   ├── views.py             # BookList API views  
│   └── urls.py              # BookList URL patterns
├── books_api/               # Main project
│   ├── settings.py          # Django settings with CORS
│   ├── urls.py              # Main URL configuration
│   ├── exceptions.py        # Custom error handling
│   └── middleware.py        # API middleware
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
└── manage.py               # Django management script
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

Run tests for specific app:
```bash
python manage.py test books
python manage.py test lists
```

## 🔍 Code Quality

This project uses [ruff](https://github.com/astral-sh/ruff) for linting and formatting.

**Check code quality:**
```bash
ruff check .
```

**Auto-fix issues:**
```bash
ruff check . --fix
```

**Format code:**
```bash
ruff format .
```

## 💾 Database

This project uses **SQLite** for development. The database file `db.sqlite3` will be created automatically when you run migrations.

To reset the database:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py loaddata initial_books.json
```
