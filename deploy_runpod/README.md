# RunPod

#### Check out our [Tutorial Blogpost](https://blog.premai.io/serverless-deploy-mistral-2-7b-runpod/)

[RunPod](https://www.runpod.io/) presents itself as a distributed GPU cloud infrastructure designed for production use. It facilitates the development, training, and scaling of AI applications while offering deployment management services. Users can rent various GPUs from RunPod at competitive rates for experimentation purposes or utilize their serverless deployment services for deploying AI-based applications.

## Pricing of RunPod

Below is the pricing structure of RunPod, updated as of March 16th, 2024. You can verify the prices [here](https://www.runpod.io/serverless-gpu).

| Capacity | Model | Price (Flex)      | Price (Active)     |
|----------|-------|-------------------|--------------------|
| 16 GB    | A4000 | $0.00020          | $0.00012           |
| 24 GB    | A5000 | $0.00026          | $0.00016           |
| 24 GB    | 4090  | $0.00044          | $0.00026           |
| 48 GB    | A6000 | $0.00048          | $0.00029           |
| 48 GB    | L40   | $0.00069          | $0.00041           |
| 80 GB    | A100  | $0.00130          | $0.00078           |
| 80 GB    | H100  | $0.00250          | $0.00150           |

RunPod offers an [online calculator](https://www.runpod.io/serverless-gpu) for estimating monthly costs based on different requirements.

## How to Get Started locally

Getting started with RunPod is straightforward. Before deploying on the platform, if you wish to try it locally, you need to install the required dependencies:

```bash
pip install -r builder/requirements.txt
```

For testing purposes, modify your `.env` file (or create one from `.env.template`) to specify a lightweight model and use CPU if no GPUs are available. For example:

```bash
MODEL_NAME="gpt2"
TOKENIZER_NAME="gpt2"
DEVICE="cpu"
```

Now you can run this setup locally using the following command:

```bash
python src/handler.py --rp_serve_api
```

This command will launch a server similar to FastAPI, allowing you to send requests and check if it is functioning correctly.
