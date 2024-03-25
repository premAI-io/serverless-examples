## Start with a base Image. We are using PyTorch v2.2 with Cuda v12.1 runtime
## when you will be using this image, it will contain all the essential cuda builds and dependencies
## so that we do not have to do it from our side. 

FROM pytorch/pytorch:2.2.1-cuda12.1-cudnn8-runtime

WORKDIR /

## We define this arguments that can be used during building the model
## if no args are defined then we will be using the default values 

ARG MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
ARG TOKENIZER_NAME=mistralai/Mistral-7B-Instruct-v0.2
ARG DEVICE=cuda
ARG MODEL_DIR=/model
ARG HF_TOKEN=null

## We set up our env variables using those arguments 

ENV MODEL_NAME=${MODEL_NAME}
ENV TOKENIZER_NAME=${TOKENIZER_NAME}
ENV DEVICE=${DEVICE}
ENV MODEL_DIR=/model
ENV HF_TOKEN=${HF_TOKEN}

## Copy the requirements txt file to install the depdendencies 
COPY requirements.txt /requirements.txt
COPY scripts/download_hf_model.py /download_hf_model.py 

## Now we install the dependencies and download the model to /model folder

RUN python3 -m pip install --upgrade -r /requirements.txt --no-cache-dir && \
    --mount=type=secret,id=HF_TOKEN,required=false \
    if [ -f /run/secrets/HF_TOKEN ]; then \
    export HF_TOKEN=$(cat /run/secrets/HF_TOKEN); \
    fi && \
    if [ -n "$MODEL_NAME" ]; then \
    python3 /download_hf_model.py; \
    fi

## Some times, the download might stuck and if that is happening then you can comment out this RUN command and the run the following command:
## However in the step: COPY ./model /model you are required to copy or download your HuggingFace model
## to ./model folder, other wise it can not access the models and face error. Now you can uncomment this below code and comment out the above one for building your container. 

# RUN python3 -m pip install -r /requirements.txt 
# COPY ./model /model

## Copy the src files to /src folder and run

COPY src /src
CMD ["python3", "-u", "/src/handler.py"]