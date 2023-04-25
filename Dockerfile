FROM python:3.9.16-slim

COPY requirements.txt /

RUN pip install -r /requirements.txt
ADD src /src

WORKDIR /src

CMD ["python", "consumer.py"]