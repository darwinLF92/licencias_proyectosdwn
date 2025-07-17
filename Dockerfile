# Imagen base
FROM python:3.10

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar dependencias y app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Puerto a exponer
EXPOSE 5000

# Comando para ejecutar
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
