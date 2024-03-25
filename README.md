# Serverless LLM Deployment Examples

This repository contains a set of hackable examples for deploying Large Language Models (LLMs) serverlessly. We'll explore and analyze three services: [Modal Labs](https://modal.com/), [Beam Cloud](https://www.beam.cloud/), and [Runpod](https://www.runpod.io/), each abstracting out the deployment process at different levels.

| Service       | Blogpost                                                    | Implementation   |
|---------------|-------------------------------------------------------------|------------------|
| Modal Labs    | [Tutorial Blogpost](https://blog.premai.io/serverless-deployment-using-huggingface-and-modal/) | [Modal Labs Deployment](/deploy_modal/) |
| Beam Cloud    | [Tutorial Blogpost](https://blog.premai.io/deploy-google-gemma-serverless-using-beam-cloud/) | [Beam Cloud Deployment](/deploy_beam/) |
| RunPod        | [Tutorial Blogpost](https://blog.premai.io/serverless-deploy-mistral-2-7b-runpod/) | [RunPod Deployment](/deploy_runpod/) |

We have blog posts for each service, as well as dedicated repositories containing full code examples and instructions on how to run and test them.

## Test Deployed Model

If you've followed our tutorials and deployed your models using any of the mentioned services, you can test the deployments from here. Please note that it can only be tested for streaming. However, if you want to make changes, feel free to do so. Before getting started, please install the requirements from here.

```bash
pip install -r requirements.txt
```

Now, assuming you deployed your model using either of the services, you can run `test.py` like this:

```bash
python3 test.py modal --url <YOUR-DEPLOYED-MODEL/BEAM-URL> --prompt "hello"
```

The above should work for Modal and Beam Cloud. For RunPod, you also need to provide the service ID like this:

```bash
python3 test.py modal --url <YOUR-DEPLOYED-RUNPOD-URL> --prompt "hello" --runpod_id <RUNPOD-ID>
```

Replace `<RUNPOD-ID>` with a value that looks like this: `80r0eh3jel99f8` (this is an example ID).