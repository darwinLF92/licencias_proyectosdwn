from django.urls import path
from .views import home, health

urlpatterns = [
    path('', home),
    path('health/', health),
]
