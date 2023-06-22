FROM python:3.8-slim
MAINTAINER Roland Zitny
COPY requirements.txt /root
RUN pip install --upgrade pip && pip install -r /root/requirements.txt
COPY feature_collector /app/feature_collector
COPY main.py /app
COPY config.py /app
WORKDIR /app
ENTRYPOINT ["/usr/local/bin/python", "/app/main.py"]