import os

# Número de procesos worker. La fórmula general es (2 x NUM_CORES) + 1
# Para Railway, con recursos limitados, 2-3 workers es apropiado
workers = 2

# Usar gevent como worker class para mejor manejo de conexiones asíncronas
# Gevent es especialmente bueno para aplicaciones con muchas operaciones I/O
worker_class = 'gevent'

# Número máximo de conexiones simultáneas que cada worker puede manejar
# 100 es un buen número para recursos limitados
worker_connections = 100

# Tiempo máximo (en segundos) que un worker puede tomar para procesar una solicitud
# Después de este tiempo, el worker será reiniciado
timeout = 120  # 120 segundos para peticiones que pueden demorar

# Tiempo (en segundos) que las conexiones keep-alive permanecerán abiertas
# Un valor bajo ayuda a liberar recursos más rápidamente
keepalive = 2

# Número de solicitudes que un worker procesará antes de reiniciarse
# Ayuda a prevenir fugas de memoria
max_requests = 1000

# Añade variación aleatoria al reinicio de workers para evitar que todos
# se reinicien al mismo tiempo
max_requests_jitter = 50

# Configuración adicional recomendada para Railway
bind = "0.0.0.0:" + os.environ.get("PORT", "8000")
workers = 2
worker_class = 'gevent'
worker_connections = 100
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50

# Configuración de logs
accesslog = "-"
errorlog = "-"
capture_output = True
enable_stdio_inheritance = True