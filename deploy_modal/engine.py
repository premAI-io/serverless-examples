import os
import asyncio
from queue import Empty
from typing import List, Union, List

# Import modal's required imports
from modal import Image, Stub, gpu, method, enter, exit

# Import the constants and HFEngine
from constants import (
    MODEL_DIR,
    BASE_MODEL,
    STUB_NAME,
    NUM_CONCURRENT_REQUESTS,
    TIMEOUT,
    GPU_COUNT,
)

# we should select our GPU config based on our Model's size
# When choosing Any then it chooses from either L4 or A10G based on availability

GPU_CONFIG = (
    gpu.A100(count=GPU_COUNT, memory=80)
    if BASE_MODEL == "mistralai/Mistral-7B-Instruct-v0.1"
    else gpu.Any(count=GPU_COUNT)
)

# an utility functions to download the model for the very first time
# when building the server and storing the model to a cache folder


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
    Image.from_registry(
        "nvidia/cuda:12.1.0-base-ubuntu22.04", add_python="3.10"
    )
    .pip_install_from_requirements("./requirements.txt")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
    .run_function(download_model_to_folder)
)

# Define the stub
stub = Stub(name=STUB_NAME)


@stub.cls(
    gpu=GPU_CONFIG,
    timeout=TIMEOUT,
    container_idle_timeout=TIMEOUT,
    allow_concurrent_inputs=NUM_CONCURRENT_REQUESTS,
    image=HF_DOCKER_IMAGE,
)
class HFEngine:
    model_name_or_path: str = MODEL_DIR
    device: str = "cuda"

    @enter()
    def start_engine(self):
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            TextIteratorStreamer,
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name_or_path, trust_remote_code=True
        ).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name_or_path, trust_remote_code=True
        )
        self.streamer = TextIteratorStreamer(self.tokenizer)
        return self

    @exit()
    def terminate_engine(self):
        import gc
        import torch

        del self.model
        torch.cuda.synchronize()
        gc.collect()

    @method()
    async def stream(
        self, chat_input: Union[str, List[dict]], generation_kwargs: dict
    ):
        from threading import Thread

        if isinstance(chat_input, str):
            chat_input = [{"role": "user", "content": chat_input}]
        input_ids = self.tokenizer.apply_chat_template(
            conversation=chat_input, tokenize=True, return_tensors="pt"
        ).to(self.device)

        gen_kwargs = dict(
            input_ids=input_ids,
            streamer=self.streamer,
            pad_token_id=self.tokenizer.eos_token_id,
            **generation_kwargs,
        )

        thread = Thread(target=self.model.generate, kwargs=gen_kwargs)
        thread.start()

        for next_token in self.streamer:
            try:
                if next_token is not None:
                    yield next_token
            except Empty:
                await asyncio.sleep(0.001)
