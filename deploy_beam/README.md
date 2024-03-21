# Beam Cloud

[Beam Cloud](https://beam.cloud) provides serverless infrastructure for deploying Machine Learning models. Most of the focus is mainly put on deploying LLMs for inference and fine-tuning and diffusion models. 

## Pricing
Here is the per/second pricing of Beam (last update: 16th March 2024). You can double check prices [here](https://www.beam.cloud/pricing). 

| GPU Model    | Price per Hour (per second) | Price per Hour (per minute) |
|--------------|-----------------------------|-----------------------------|
| T4 GPU       | $0.000172                   | $0.62                       |
| L4 GPU       | $0.000272                   | $0.98                       |
| A10G GPU     | $0.000467                   | $1.68                       |
| A100-80 GPU  | $0.001774                   | $6.38                       |

`Please note`: A100 GPUs are not readily available. You have to mail Beam in order to get access. 

The way beam works is kind of similar to Beam. It provides an interface abstracting out the docker file and deployement process. Once you define all those, then in this example, we show you how you can develope a custom Beam deployement using FastAPI under the hood. Since beam readily supports Fast API, so it opens door to several application level customization. However the problem we saw is, it is still super early stage and it does not provide very good documentation to carry out those customization. 

## How to get started

Getting started with Beam is super easy.

```bash
# Install the main beam SDK

curl https://raw.githubusercontent.com/slai-labs/get-beam/main/get-beam.sh -sSfL | sh

# After this install the python sdk

python3 -m pip install --upgrade beam-sdk
```

Once done, make sure you have an account on Beam. Once done, you can use this repo or customize it according to your needs. In order to run, all you have to do is:

```bash
beam serve server.py

# or
beam deploy server.py
```

This will serve/deploy your HuggingFace Model. The key difference is, when you use `beam serve` than can see the build process all from your terminal and you sent your files temporarily to Beam. This makes the deployment temporary. It helps when you have written your code initially and want to test. Here is how you can serve the model. In `deploy` you send all your files to Beam and it is deployed. After this you can manage (like watching logs / deleting app) all through Beams's python CLI or inside their app. Once done it will open a browser window, showing you the deployement with all the metrics and essential post deployement KPIs.