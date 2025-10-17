from  rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    view = context.get("view", None)
    view_name = view.__class__.__name__ if view else "UnknownView"

    if response is not None:

        logger.warning(
            f"[{view_name} {exc.__class__.__name__}: {response.data}]",
            exc_info=True,
            extra={"status_code": response.status_code}
        )

        return Response({
            "success": False,
            "error": {
                "message": response.data.get("detail") if "detail" in response.data else response.data,
                "status_code": response.status_code
            }
        },status = response.status_code)
    
    logger.error(
            f"[{view_name}] Unexpected Error: {str(exc)} ",
            exc_info=True
        )
    
    return Response({
        "success": False,
        "error": {
            "message": str(exc),
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)