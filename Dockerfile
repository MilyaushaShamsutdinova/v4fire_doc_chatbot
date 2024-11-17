FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./setup.py /app/setup.py
COPY ./requirements.txt /app/requirements.txt
COPY ./database /app/database
COPY ./src /app/src
# COPY .env /app/.env

RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt \
    && pip install -e . \
    && python -m spacy download en_core_web_sm


ENV PYTHONPATH=/app

CMD ["python", "src/frontend/main.py"]