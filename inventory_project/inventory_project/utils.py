from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        logger.error(f"Exception: {exc} | Context: {context}")
        customized_response = {
            'error': {
                'message': str(exc),
                'status_code': response.status_code
            }
        }
        return Response(customized_response, status=response.status_code)
    else:
        logger.error(f"Unhandled exception: {exc} | Context: {context}")
        return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
