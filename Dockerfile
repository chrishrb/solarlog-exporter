FROM python:3.9.1-alpine3.12 as base
WORKDIR /solarlog_exporter
COPY requirements.txt /solarlog_exporter
RUN pip3 install -r requirements.txt

FROM base as src
ADD solarlog_exporter /solarlog_exporter

FROM src as test
COPY tests /solarlog_exporter
COPY requirements.dev.txt /solarlog_exporter
RUN pip3 install -r requirements.dev.txt
RUN python3 -m pytest

FROM src as prod
ENTRYPOINT ["python3"]
CMD ["main.py"]