
FROM python:3.10 AS builder
COPY requirements.txt .

RUN pip install -r requirements.txt

FROM python:3.10-slim
WORKDIR /code

<<<<<<< HEAD
COPY --from=builder /root/.local /root/.local
=======
COPY —from=builder /root/.local /root/.local
>>>>>>> 83bd1a5d4ed265b1872eb238ddfc4bf61a86af39
ADD db/ db/
ADD cogs/ cogs/
COPY ./ .
ENV PATH=/root/.local:$PATH

CMD ["python3", "main.py"]
