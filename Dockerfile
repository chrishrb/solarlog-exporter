FROM python:3.9.1-alpine3.12

ADD requirements.txt /app/requirements.txt

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN set -ex \
    && apk add --no-cache --virtual .build-deps postgresql-dev build-base \
       libressl-dev musl-dev libffi-dev \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt \
    && runDeps="$(scanelf --needed --nobanner --recursive /env \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | sort -u \
        | xargs -r apk info --installed \
        | sort -u)" \
    && apk add --virtual rundeps $runDeps \
    && apk del .build-deps

ADD solarlog_exporter /app/solarlog_exporter
ADD main.py /app/main.py

WORKDIR /app

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ENTRYPOINT ["python3", "main.py"]