import os

# Número de procesos worker. Fórmula general: (2 x NUM_CORES) + 1
# Railway: valores pequeños como 2 están bien
workers = 2

# Usar worker sync (por defecto en Gunicorn)
worker_class = 'sync'

# Tiempo máximo (en segundos) que un worker puede tomar para procesar una solicitud
timeout = 30  # más de esto puede hacer que Railway cierre la app

# Tiempo que las conexiones keep-alive permanecen abiertas
keepalive = 2

# Reiniciar workers después de cierto número de solicitudes (por seguridad/memoria)
max_requests = 1000
max_requests_jitter = 50

# Bind al puerto dinámico proporcionado por Railway
bind = "0.0.0.0:" + os.environ.get("PORT", "8000")

# Logs
accesslog = "-"
errorlog = "-"
capture_output = True
enable_stdio_inheritance = True
