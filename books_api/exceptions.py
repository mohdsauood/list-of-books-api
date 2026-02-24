"""Custom exception handler for DRF."""

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF.

    Formats all error responses consistently with:
    - error: True/False
    - message: Human readable error message
    - code: HTTP status code
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # If there is an error, format it to standard format
    if response is not None:
        response.data = {
            "error": True,
            "message": response.data.get('detail', 'Something went wrong'),
            "code": response.status_code
        }

    return response
