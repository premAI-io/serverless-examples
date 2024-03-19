FROM python:latest

ARG MODEL_NAME="stabilityai/stablelm-zephyr-3b"
ARG TOKENIZER_NAME="stabilityai/stablelm-zephyr-3b"
ARG DEVICE="cuda"

COPY builder/requirements.txt /requirements.txt
COPY builder/setup.sh /setup.sh

RUN python3 -m pip install --upgrade -r /requirements.txt --no-cache-dir

COPY src /src
CMD ["python", "/src/handler.py"]