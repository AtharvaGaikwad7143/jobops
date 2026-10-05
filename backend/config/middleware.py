import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(
            "Incoming request: %s %s",
            request.method,
            request.path,
        )

        response = self.get_response(request)

        logger.info(
            "Response status: %s",
            response.status_code,
        )

        return response