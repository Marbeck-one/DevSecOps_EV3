FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ejecutamos la creación de la DB al construir (para este lab)
RUN python create_db.py

EXPOSE 5000

CMD ["python", "secure_app.py"]
