# Serverless LLM Deployment Examples

This repository contains a set of examples for deploying Large Language Models (LLMs) serverlessly. We'll be exploring and analyzing three services: [Modal Labs](https://modal.com/), [Beam Cloud](https://www.beam.cloud/), and [Runpod](https://www.runpod.io/), each abstracting out the deployment process at different levels.

We'll evaluate these services based on:

1. **Metrics**: This includes metrics like latency, cost per hour or per second of usage.
2. **Quality/Level of Abstraction**: We'll assess the tradeoff between flexibility and customization versus the ease of running applications.
3. **Reliability**: Here, we'll consider:
   - The availability of preferred GPUs.
   - Handling of cold start issues.
   - Support for handling concurrent requests and average latency during deployment.

## 🔭 Scope of the Repository

This repository serves developers in three key ways:

1. **Understanding Serverless Deployments**: Developers can grasp how serverless deployments are facilitated by services like Modal, Runpod, and Beam.
2. **Understanding Tradeoffs**: By examining the provided examples, developers can understand the tradeoffs inherent in different serverless deployment approaches.
3. **Learning and Extending**: The examples provided here can be used as a learning resource, and developers can extend them for their own use cases and applications.

## 🔄 Experiment Workflow

To ensure a fair comparison, we'll adhere to this deployment workflow:

### Application Workflow 

1. The inference engine logic will utilize simple HuggingFace pipelines to deploy `Mistral 7B Instruct` by Mistral AI and `stabilityai/stablelm-zephyr-3b` by Stability AI. We do the benchmarking for A100 and A10 GPUs. For some providers like Beam, A100s are not readily available. So for that A100 benchmarks are used for only Mistral 7B instruct model and for A10G we use Stable LM.  
2. We will create a chat service with streaming capabilities.
3. Deploy the service.

### Experiment and benchmarking workflow

1. Once served / deployed, we will be using 30 prompts, where the first 5 prompts are used to evaluate the warmup or cold start latency and timings, and leftover 25 prompts are used to see the benchmarks on normal queues (after cold start)

2. Generation length will be set to 512 tokens

3. For each completions, we will try to evaluate:

    - Pricing
    - tokens/sec and latency (cold start and average)

Each deployment method has its own folder, with accompanying README files providing instructions and additional information about usage.

Also, before getting started, please make sure you created a virtual env and installed the common dependencies. Here is how you can do it.

```bash

# create a virtual env
python -m venv venv

# activate it
source venv/bin/activate

# now install the common dependencies
pip install -r requirements.txt

```