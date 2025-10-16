from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return Response({
            "success": False,
            "error": {
                "message": response.data.get("detail") if "detail" in response.data else response.data,
                "status_code": response.status_code
            }
        },
        status=response.status_code)
    
    return Response({
        "success": False,
        "error": {
            "message": str(exc),
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    },
    status=status.HTTP_500_INTERNAL_SERVER_ERROR)