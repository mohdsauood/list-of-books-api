#!/usr/bin/env python
"""
Simple script to test the API endpoints.
Run this after starting the Django server.
"""

import sys

import requests


def test_api():
    """Test the main API endpoints."""
    base_url = "http://localhost:8000/api"

    print("🚀 Testing Book List API")
    print("=" * 50)

    # Test 1: Get all books
    print("\n1. Testing GET /api/books/")
    try:
        response = requests.get(f"{base_url}/books/")
        if response.status_code == 200:
            books = response.json()
            print(f"✅ Success! Found {len(books)} books")
            if books:
                print(f"   First book: {books[0]['title']} by {books[0]['author']}")
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Is the server running?")
        print("   Run: python manage.py runserver")
        return False

    # Test 2: Create a new book
    print("\n2. Testing POST /api/books/")
    new_book = {
        "title": "Test Book",
        "author": "Test Author",
        "year": 2025
    }

    response = requests.post(f"{base_url}/books/", json=new_book)
    if response.status_code == 201:
        created_book = response.json()
        print(f"✅ Book created! ID: {created_book['id']}")
        book_id = created_book['id']
    else:
        print(f"❌ Error creating book: {response.status_code}")
        return False

    # Test 3: Get all lists (should be empty initially)
    print("\n3. Testing GET /api/lists/")
    response = requests.get(f"{base_url}/lists/")
    if response.status_code == 200:
        lists = response.json()
        print(f"✅ Success! Found {len(lists)} lists")
    else:
        print(f"❌ Error: {response.status_code}")
        return False

    # Test 4: Create a new list
    print("\n4. Testing POST /api/lists/")
    new_list = {
        "name": "My Test List",
        "description": "A test list of books",
        "bookIds": [book_id]  # Add our newly created book
    }

    response = requests.post(f"{base_url}/lists/", json=new_list)
    if response.status_code == 201:
        created_list = response.json()
        print(f"✅ List created! ID: {created_list['id']}")
        print(f"   Books in list: {len(created_list['bookIds'])}")
        list_id = created_list['id']
    else:
        print(f"❌ Error creating list: {response.status_code}")
        return False

    # Test 5: Get list details
    print("\n5. Testing GET /api/lists/{id}/")
    response = requests.get(f"{base_url}/lists/{list_id}/")
    if response.status_code == 200:
        list_detail = response.json()
        print("✅ List details retrieved!")
        print(f"   List name: {list_detail['name']}")
        print(f"   Books: {len(list_detail['books'])}")
        if list_detail['books']:
            print(f"   First book: {list_detail['books'][0]['title']}")
    else:
        print(f"❌ Error getting list details: {response.status_code}")
        return False

    print("\n🎉 All tests passed! API is working correctly.")
    print("\nYou can now:")
    print("- Connect your Angular frontend")
    print("- View the admin at http://localhost:8000/admin/")
    print("- Check API docs in the README.md")

    return True


if __name__ == "__main__":
    if not test_api():
        sys.exit(1)
