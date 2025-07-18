from django.urls import path
from .views import home, health, debug_info

urlpatterns = [
    path('', home),
    path('health/', health),
    path("debug/", debug_info),  # <-- solo mientras estás en pruebas
]
