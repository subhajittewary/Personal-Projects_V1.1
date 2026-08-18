FROM python:3.12-slim

WORKDIR /app
COPY health_server.py /app/health_server.py

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
CMD ["python", "/app/health_server.py"]
