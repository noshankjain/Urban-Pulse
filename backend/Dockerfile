# backend/Dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN pip install fastapi uvicorn sqlalchemy psycopg2-binary geoalchemy2
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]