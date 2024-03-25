# Modal Labs 
#### Check out our [Tutorial Blogpost](https://blog.premai.io/serverless-deployment-using-huggingface-and-modal/)

[Modal Labs](https://modal.com/) offers dedicated GPU and infrastructure primarily focused on facilitating serverless deployments of models. Its key features include providing serverless deployments for Large Language Models (LLMs) and image models, as well as fine-tuning LLMs.

## Pricing
Below is the pricing structure of Modal Labs, updated as of March 16th, 2024. You can verify the prices [here](https://www.modal.com/pricing).

| Model              | Price (per sec)   | Price (per hour)   |
|--------------------|--------------------|-------------------|
| Nvidia H100        | $0.002125          | $7.65             |
| Nvidia A100, 80 GB | $0.001553          | $5.59             |
| Nvidia A100, 40 GB | $0.001036          | $3.73             |
| Nvidia A10G        | $0.000306          | $1.10             |
| Nvidia L4          | $0.000291          | $1.05             |
| Nvidia T4          | $0.000164          | $0.59             |

Modal simplifies the MLOps side of model deployment by providing a convenient Python interface. Unlike other platforms like runpod, you don't need to handle Dockerfiles or Docker compose files for server building. Instead, you only need to define essential elements in the Dockerfile, such as the base image and dependencies. For example, you can find a detailed example [here](/modal/server.py).

## Getting Started
Getting started with Modal is straightforward. Simply install Modal using pip:

```bash
pip install -U modal
```

After installation, you can choose to either use `modal serve` or `modal deploy`. The key difference lies in the deployment process. When using `modal serve`, you can monitor the build process directly from your terminal, and your files are temporarily sent to Modal. This temporary deployment is useful for initial code testing. Here's how you can serve the model:

```bash
modal serve server.py
```

On the other hand, `deploy` sends all your files to Modal for deployment. Once deployed, you can manage various aspects, such as watching logs and deleting apps, either through Modal's Python CLI or within their app.
