# Extend ml-base
FROM marcusacheema/keybert-base:v1.0 AS keybert-stage
FROM marcusacheema/openai-base:v1.0 AS openai-stage

FROM python:3.12-slim

WORKDIR /app

COPY --from=keybert-stage /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=openai-stage /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy and install application-specific requirements
COPY requirements-app.txt .
RUN pip install --no-cache-dir -r requirements-app.txt

# Copy application code
COPY . /app

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]


# RUN python -c "import openai; print('OpenAI version')"
# RUN python -c "from keybert import KeyBERT; print('KeyBERT version:')"