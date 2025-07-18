import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

@api_view(["GET"])
def home(request):
    try:
        return Response({"message": "API en Django funcionando"}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error en la vista 'home': {str(e)}")
        return Response({"error": "Error interno en el servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def health(request):
    try:
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error en la vista 'health': {str(e)}")
        return Response({"error": "Error interno en el servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def debug_info(request):
    return Response({
        "debug": os.environ.get("DEBUG"),
        "port": os.environ.get("PORT"),
        "allowed_hosts": os.environ.get("ALLOWED_HOSTS"),
        "working_dir": os.getcwd()
    })