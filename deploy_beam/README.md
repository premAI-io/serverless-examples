# Beam Cloud 
#### Check out our [Tutorial Blogpost](https://blog.premai.io/deploy-google-gemma-serverless-using-beam-cloud/)

[Beam Cloud](https://beam.cloud) offers serverless infrastructure for deploying Machine Learning models, with a primary focus on deploying Large Language Models (LLMs) for inference and fine-tuning, as well as diffusion models.

## Pricing
Below is the pricing structure of Beam, updated as of March 16th, 2024. You can verify the prices [here](https://www.beam.cloud/pricing).

| GPU Model    | Price per Hour (per second) | Price per Hour (per minute) |
|--------------|-----------------------------|-----------------------------|
| T4 GPU       | $0.000172                   | $0.62                       |
| L4 GPU       | $0.000272                   | $0.98                       |
| A10G GPU     | $0.000467                   | $1.68                       |
| A100-80 GPU  | $0.001774                   | $6.38                       |

*Note:* A100 GPUs are not readily available; you need to contact Beam to gain access.

Beam simplifies the deployment process by abstracting the Dockerfile and deployment procedures. In this example, we demonstrate how to develop a custom deployment using FastAPI under the hood. While Beam supports FastAPI, enabling various application-level customizations, the documentation for these customizations is currently lacking due to the platform being in an early stage of development.

## How to Get Started
Getting started with Beam is straightforward:

```bash
# Install the main Beam SDK
curl https://raw.githubusercontent.com/slai-labs/get-beam/main/get-beam.sh -sSfL | sh

# After this, install the Python SDK
python3 -m pip install --upgrade beam-sdk
```

Once installed, ensure you have an account on Beam. You can then use the provided repository or customize it according to your needs. To run, simply execute:

```bash
beam serve server.py

# or

beam deploy server.py
```

This command will serve/deploy your HuggingFace Model. The key difference between `beam serve` and `beam deploy` lies in the deployment process. With `beam serve`, you can monitor the build process directly from your terminal, and your files are temporarily sent to Beam, making the deployment temporary. This feature is useful for initial code testing. In contrast, `beam deploy` sends all your files to Beam for deployment. Once deployed, you can manage various aspects, such as watching logs and deleting apps, either through Beam's Python CLI or within their app. After deployment, a browser window will open, displaying the deployment along with essential post-deployment Key Performance Indicators (KPIs).