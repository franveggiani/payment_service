FROM python:3.11-slim

# Evitar buffering para ver logs en tiempo real
ENV PYTHONUNBUFFERED=1

# Creamos el directorio de trabajo
WORKDIR /app

# Instalamos las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el proyecto
COPY . .

# Exponemos el puerto
EXPOSE 8005

# Arrancamos el servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005", "--reload"]
