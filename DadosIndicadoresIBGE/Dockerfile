FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
        pandas \
        requests \
        sqlalchemy \
        psycopg2-binary

ENV DB_USER=postgres \
    DB_PASS=teste123 \
    DB_HOST=db \
    DB_PORT=5432 \
    DB_NAME=db_ibge

CMD ["python", "TesteDadosIBGE.py"]
