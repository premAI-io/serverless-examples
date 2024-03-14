# RunPod

[RunPod](https://www.runpod.io/) is a distributed GPU cloud infrastructure built for production. It helps us to develop, train, and scale AI applications easily and also helps to manage deployements. You can also rent different GPUs using runpod for very lesser rates to carry out your experiments or use their serverless deployements services to deploy AI based applications. 

## Pricing of RunPod

| Capacity | Model | Price (Flex)      | Price (Active)     |
|----------|-------|-------------------|--------------------|
| 16 GB    | A4000 | $0.00020          | $0.00012           |
| 24 GB    | A5000 | $0.00026          | $0.00016           |
| 24 GB    | 4090  | $0.00044          | $0.00026           |
| 48 GB    | A6000 | $0.00048          | $0.00029           |
| 48 GB    | L40   | $0.00069          | $0.00041           |
| 80 GB    | A100  | $0.00130          | $0.00078           |
| 80 GB    | H100  | $0.00250          | $0.00150           |

They also have an [awesome calculator](https://www.runpod.io/serverless-gpu) which helps us to do a monthly costs based on different requirements. 

## How to get started

Getting started with runpod is super easy. Before deploying on the platform, if you want to try this out locally you need to first install the given requirements. 

```bash
pip install -r builder/requirements.txt
```

Since you will be doing testing, so change your `.env` (or make one from `.env.template`) such that model is super light and using cpu (if you do not have GPUs). Something like this.

```bash
HF_MODEL_NAME="gpt2"
HF_TOKENIZER_NAME="gpt2"
DEVICE="cpu"
```

Now you can run this setup locally using the following command:

```bash
python src/handler.py --rp_serve_api
```

This will serve a fastapi like server and then you can post requests and check if it is working or not. 