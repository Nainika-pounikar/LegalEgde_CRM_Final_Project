import logging

from django.conf import settings
from django.core.exceptions import DisallowedHost
from django.http import JsonResponse


logger = logging.getLogger(__name__)


class APIExceptionMiddleware:
    """
    Ensure API errors are JSON in production so frontend clients do not fail with
    JSON parsing errors when Django returns HTML error pages.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as exc:
            if not request.path.startswith('/api/'):
                raise

            if settings.DEBUG:
                raise

            if isinstance(exc, DisallowedHost):
                return JsonResponse(
                    {'error': 'Invalid host configuration. Check ALLOWED_HOSTS.'},
                    status=400,
                )

            logger.exception('Unhandled API exception on %s', request.path)
            return JsonResponse(
                {'error': 'Internal server error. Please try again.'},
                status=500,
            )
