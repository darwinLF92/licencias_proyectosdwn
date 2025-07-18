import logging
import os
import traceback
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from decouple import config

logger = logging.getLogger(__name__)

@api_view(["GET"])
def home(request):
    try:
        return Response({"message": "API en Django funcionando"}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error en la vista 'home': {str(e)}\n{traceback.format_exc()}")
        return Response({"error": "Error interno en el servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def health(request):
    try:
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error en la vista 'health': {str(e)}\n{traceback.format_exc()}")
        return Response({"error": "Error interno en el servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def debug_info(request):
    try:
        debug_data = {
        "debug": config("DEBUG", default=None),
        "port": config("PORT", default=None),
        "allowed_hosts": config("ALLOWED_HOSTS", default=None),
        "working_dir": os.getcwd(),
        "settings_module": os.environ.get("DJANGO_SETTINGS_MODULE")
        }
        return Response(debug_data, status=status.HTTP_200_OK)
    except Exception as e:
            logger.error(f"Error en la vista 'debug_info': {str(e)}")
            return Response({"error": "No se pudo obtener la información de entorno"}, status=500)
