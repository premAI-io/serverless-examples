NAME = "beam-stable-lm-3b-deployement-a10g"
CPU = 4
GPU = "A10G"
PACKAGES = [
    "huggingface_hub==0.19.4",
    "hf-transfer==0.1.4",
    "torch==2.1.2",
    "transformers",
    "datasets",
    "accelerate",
    "fastapi",
]
PYTHON_VERSION = "python3.9"
CACHE_PATH = "./cached_models"
MODEL_ID = "stabilityai/stablelm-zephyr-3b"
