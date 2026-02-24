"""Custom middleware for API error handling."""

from django.http import JsonResponse


class APIErrorMiddleware:
    """Convert HTML error responses to JSON for API endpoints."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)

    def process_response(self, request, response):
        """Convert HTML errors to JSON for API requests."""
        # Only handle API paths
        if not request.path.startswith('/api/'):
            return response

        # Check if it's an error status (4xx or 5xx)
        if response.status_code >= 400:
            # Check if response is HTML (Django error page)
            content_type = response.get('Content-Type', '')

            # If it's already JSON (from DRF), let it through
            if 'application/json' in content_type:
                return response

            # Convert HTML to JSON for API endpoints
            return JsonResponse(
                {
                    "error": True,
                    "message": "Not found." if response.status_code == 404 else "Error",
                    "code": response.status_code,
                },
                status=response.status_code
            )

        return response
