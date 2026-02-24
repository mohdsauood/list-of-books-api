"""App configuration for books."""

from django.apps import AppConfig
from django.db.models.signals import post_migrate


class BooksConfig(AppConfig):
    """Configuration for books app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'

    def ready(self):
        """Run setup tasks when app is ready."""
        def load_initial_data(sender, **kwargs):
            """Auto-load initial books after migration."""
            from books.models import Book

            if not Book.objects.exists():
                try:
                    from django.core.management import call_command
                    call_command('loaddata', 'books/fixtures/initial_books.json', verbosity=0)
                except Exception:
                    # Silent fail if fixture doesn't exist
                    pass

        post_migrate.connect(load_initial_data, sender=self)
