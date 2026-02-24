"""Management command to load initial books data."""

from django.core.management import call_command
from django.core.management.base import BaseCommand

from books.models import Book


class Command(BaseCommand):
    help = 'Load initial books data if database is empty'

    def handle(self, *args, **options):
        """Load initial data only if no books exist."""
        # Only load if no books exist
        if Book.objects.exists():
            self.stdout.write(
                self.style.WARNING('Books already exist. Skipping initial data load.')
            )
            return

        try:
            call_command('loaddata', 'books/fixtures/initial_books.json')
            self.stdout.write(
                self.style.SUCCESS('Successfully loaded initial books data')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to load initial data: {e}')
            )
