
FROM python:3.10 AS builder
COPY requirements.txt .

RUN pip install -r requirements.txt

FROM python:3.10-slim
WORKDIR /code

ADD db/ db/
ADD cogs/ cogs/
COPY ./ .
ENV PATH=/root/.local:$PATH

CMD ["python3", "main.py"]
