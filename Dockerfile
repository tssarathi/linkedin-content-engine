## Parent image
FROM python:3.11-slim

## Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## Work directory inside the docker container
WORKDIR /app

## Installing system dependancies
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Copy all contents from local to app
COPY . .

## Run pyproject.toml
RUN pip install --no-cache-dir -e . && \
    streamlit --version

# Used PORTS
EXPOSE 8501
EXPOSE 8000

# Run the app
CMD ["python", "main.py"]
