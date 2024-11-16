# Backend Dockerfile (Flask)
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy Source Code
COPY . .

# Expose Port
EXPOSE 5000

# Run the app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]


# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#     build-essential \
#     libpq-dev && \
#     rm -rf /var/lib/apt/lists/*