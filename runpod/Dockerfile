# We will use a base image by runpod which handles all the cuda depdencies.

FROM runpod/base:0.4.0-cuda11.8.0

# We have the three arguments Modal name, Tokenizer name and device
# this will help us to swap in swap out any model during deployement

ARG MODEL_NAME=""
ARG TOKENIZER_NAME=""
ARG DEVICE=""

# Setting this argument as env variable

ENV MODEL_NAME=$MODEL_NAME \
    TOKENIZER_NAME=$TOKENIZER_NAME \
    DEVICE=$DEVICE 

# Copy the setup.sh and requirements.txt file from builder to install different system and python dependencies

COPY builder/setup.sh /setup.sh
COPY builder/requirements.txt /requirements.txt
COPY builder/download_model.py /download_model.py

RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install --upgrade -r /requirements.txt --no-cache-dir && \
    --mount=type=secret,id=HF_TOKEN,required=false \
    if [ -f /run/secrets/HF_TOKEN ]; then \
    export HF_TOKEN=$(cat /run/secrets/HF_TOKEN); \
    fi && \
    if [ -n "$MODEL_NAME" ]; then \
    python3 /download_model.py; \
    fi

# Add all the source files and start the handler

COPY src /src
CMD ["python3", "/src/handler.py"]