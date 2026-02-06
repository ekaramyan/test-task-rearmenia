FROM python:3.10

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    GIT_ASKPASS=echo


WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip setuptools && \
    pip install -r requirements.txt

COPY . .

RUN find . -type d -name "__pycache__" -exec rm -rf {} + && \
    find . -type f -name "*.pyc" -delete
