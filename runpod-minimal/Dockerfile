FROM python:3.11.1-buster

WORKDIR /

ARG MODEL_NAME="stabilityai/stablelm-zephyr-3b"
ARG TOKENIZER_NAME="stabilityai/stablelm-zephyr-3b"
ARG DEVICE="cuda"

COPY builder/requirements.txt .

RUN pip install -r requirements.txt

COPY src /src
CMD ["python", "-u", "/src/handler.py"]
