# Modal Labs

[Modal Labs](https://modal.com/) provides dedicated GPU and infrastructure mainly focussed for doing serverless deployments of models. Some of it's key features include providing serverless deployments for LLMs and image models, fine-tuning LLMs etc. 


## Pricing
Here is the per/second pricing of Modal

| Model              | Price (per sec)   | Price (per hour)   |
|--------------------|--------------------|-------------------|
| Nvidia H100        | $0.002125          | $7.65             |
| Nvidia A100, 80 GB | $0.001553          | $5.59             |
| Nvidia A100, 40 GB | $0.001036          | $3.73             |
| Nvidia A10G        | $0.000306          | $1.10             |
| Nvidia L4          | $0.000291          | $1.05             |
| Nvidia T4          | $0.000164          | $0.59             |

An awesome thing about Modal is that, you do not have to do the heaving lifting to do the MLOps side of things for deploying models on Modal. Modal provides a nice python interface to handle those. For instance, unlike runpod, you do not have to Dockerfiles or Docker compose files in order to build the server. Instead all you need is to define the most required things that you feel are required inside the Dockerfile. For example, the base image, depdencies to install etc. You can find a detailed example of this [here](/modal/server.py)

## How to get started
Getting started with modal is super easy. All you need to do is install modal.

```bash
pip install -U modal
```

After this you can either do `modal serve` or `modal deploy`. The key difference is, when you use `modal serve` than can see the build process all from your terminal and you sent your files temporarily to Modal. This makes the deployment temporary. It helps when you have written your code initially and want to test. Here is how you can serve the model. 

```bash
modal serve server.py
```

In `deploy` you send all your files to Modal and it is deployed. After this you can manage (like watching logs / deleting app) all through modal's python CLI or inside their app. 
