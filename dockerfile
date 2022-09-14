FROM python:3.10 AS builder

FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

ADD db/ db/
ADD cogs/ cogs/
COPY ./ .
ENV PATH=/root/.local:$PATH

CMD ["python3", "main.py"]
