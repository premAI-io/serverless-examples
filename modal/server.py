import os 
import json
from typing import Union, List
from pydantic import BaseModel, Field 
from fastapi.responses import StreamingResponse

from modal import Image, Stub, gpu, web_endpoint

from engine import HFEngine
from constants import MODEL_DIR, BASE_MODEL

GPU_CONFIG = gpu.A100(memory=80, count=1)

# Start with making some utility functions to download the model

def download_model_to_folder():
    from huggingface_hub import snapshot_download
    from transformers.utils import move_cache

    os.makedirs(MODEL_DIR, exist_ok=True)

    snapshot_download(
        BASE_MODEL,
        local_dir=MODEL_DIR,
        ignore_patterns=["*.pt"],  # Using safetensors
    )
    move_cache()

# After this define the Image 
# Under the hood, this acts as an interface with your docker file that will be used during the time of deployement

HF_DOCKER_IMAGE = (
    Image.from_registry("nvidia/cuda:12.1.0-base-ubuntu22.04", add_python="3.10").pip_install(
        "transformers==4.38.0",
        "huggingface_hub==0.19.4",
        "hf-transfer==0.1.4",
        "torch==2.1.2",
        "einops==0.7.0",
        "tiktoken==0.6.0",
    )
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
    .run_function(download_model_to_folder)
)

# Define a stub
# Just to maintain some level of best practices we are decoupling the HFEngine
# with ModalHuggingFaceDeployment, we could have done it in the same file if we want

stub = Stub(name="mistral-7b-deployment")

@stub.cls(
    gpu=GPU_CONFIG,
    timeout=60 * 10,
    container_idle_timeout=60 * 10,
    allow_concurrent_inputs=10,
    image=HF_DOCKER_IMAGE,
)
class ModalHuggingFaceDeployment(HFEngine):
    model_name_or_path: str = MODEL_DIR
    device: str = "cuda"


# Finally initialize the server 
# Inside the JobInput you can add more input fields according to your choice
    
class JobInput(BaseModel):
    messages: Union[str, List[dict]]
    max_new_tokens: int | None = Field(default=512)
    temperature: float | None = Field(default=0.7)
    top_p: float | None = Field(default=0.95)


@stub.function(keep_warm=1, allow_concurrent_inputs=10, timeout=60 * 10, image=HF_DOCKER_IMAGE)
@web_endpoint(method="POST", label="completion")
async def completion(item: JobInput):
    model = ModalHuggingFaceDeployment()
    gen_kwargs = {
        "max_new_tokens": item.max_new_tokens,
        "temperature": item.temperature,
        "top_p": item.top_p,
    }

    async def _stream_completion():
        async for text in model.stream.remote_gen.aio(
            chat_input=item.messages, generation_kwargs=gen_kwargs
        ):
            yield f"data: {json.dumps(dict(text=text), ensure_ascii=False)}\n\n"
    
    return StreamingResponse(_stream_completion(), media_type="text/event-stream")