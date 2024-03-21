FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-runtime

WORKDIR /

ARG MODEL_NAME=stabilityai/stablelm-zephyr-3b
ARG TOKENIZER_NAME=stabilityai/stablelm-zephyr-3b
ARG DEVICE=cuda
ARG MODEL_DIR=/model

ENV MODEL_NAME=${MODEL_NAME}
ENV TOKENIZER_NAME=${TOKENIZER_NAME}
ENV DEVICE=${DEVICE}
ENV MODEL_DIR=/model


COPY requirements.txt /requirements.txt
RUN python3 -m pip install -r /requirements.txt
COPY ./model /model
COPY src /src

CMD ["python3", "-u", "/src/handler.py"]