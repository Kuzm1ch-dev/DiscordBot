FROM python:3.10 AS builder
COPY requirements.txt .
ADD . /cogs
ADD . /db

RUN pip install --user -r requirements.txt

FROM python:3.10-slim
WORKDIR /code

COPY --from=builder /root/.local /root/.local
COPY ./src .

ENV PATH=/root/.local:$PATH

CMD ["python", "-u", "./main.py"]