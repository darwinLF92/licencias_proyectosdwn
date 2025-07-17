# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expone el puerto definido por Railway
EXPOSE 8080

# Comando para ejecutar la app con gunicorn
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:8080"]
