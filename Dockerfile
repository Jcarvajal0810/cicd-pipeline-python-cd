# Dockerfile
# Usa una imagen base oficial de Python. Elige una versión específica para consistencia.
FROM python:3.13-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia solo el archivo de requerimientos primero para aprovechar el cache de Docker
COPY requirements.txt .

# Instala solo las dependencias de ejecución (Flask, Flask-WTF y Gunicorn).
# --require-hashes: solo instala las versiones exactas del lock y verifica su hash.
# --only-binary :all: solo instala wheels, sin ejecutar scripts setup.py.
# --no-cache-dir reduce el tamaño de la imagen.
RUN pip install --no-cache-dir --only-binary :all: --require-hashes -r requirements.txt

# Copia el código de la aplicación (solo la carpeta app)
COPY app/ ./app/

# Crea un usuario sin privilegios y ejecuta la aplicación con él (no como root)
RUN useradd --create-home --uid 10001 appuser
USER appuser

# Expón el puerto en el que Gunicorn servirá la aplicación
EXPOSE 8000

# Gunicorn con 4 workers escuchando en el puerto 8000 del contenedor.
# --preload carga la app una sola vez antes de crear los workers, así todos
# comparten la misma SECRET_KEY si no se define por variable de entorno.
CMD ["gunicorn", "--workers=4", "--preload", "--bind=0.0.0.0:8000", "app.app:app"]
