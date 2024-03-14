from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer

def download_model(model_name: str):
    AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path=model_name)
    AutoTokenizer.from_pretrained(pretrained_model_name_or_path=model_name)

if __name__ == "__main__":
    download_model()