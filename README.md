# Serverless LLM Deployment Examples

This repository contains a set of examples for deploying Large Language Models (LLMs) serverlessly. We'll be exploring and analyzing three services: [Modal Lab](https://modal.com/), [Beam Cloud](https://www.beam.cloud/), and [Runpod](https://www.runpod.io/), each abstracting out the deployment process at different levels.

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

1. The inference engine logic will utilize simple HuggingFace pipelines to deploy Mistral 7B Instruct. 
2. We will create a chat service with streaming capabilities.
3. Deploy the service.

### Experiment and benchmarking workflow

1. Once served / deployed, we will be using 30 prompts, where the first 5 prompts are used to evaluate the warmup or cold start latency and timings, and leftover 25 prompts are used to see the benchmarks on normal queues (after cold start)

2. Generation length will be set to 512 tokens

3. For each completions, we will try to evaluate:

    - Pricing
    - tokens/sec and latency (cold start and average)

Each deployment method has its own folder, with accompanying README files providing instructions and additional information about usage.

## 🧐 Analysis and Results 

In this section we are going to analyse some benchmarks and some overall thoughts while building the application. 

### Modal

1. **Costs:** The approx cost that took for the experiment in an A100-80 GB for 30 prompts (3 during Cold Start and 27 after that) was around 0.7 $. When it comes to latency, the average cold start latency was around 24.8 ms and after that average latency was around 14.45 ms. So roughly it takes ~ 10 seconds to get the server ready before it takes the first request. 

2. **Quality/Level of Abstraction**: When it comes to Modal, it is super easy to start deploying your model of choice. It gives a nice abstractions on creating docker files through their python interfaces. However, when it comes to huge amount of customisation (from ground up), users might have to go through the documentation more to understand nuances associated with the abstract which could be a potential tradeoff with low level customization. But Modal seems to be super developer friendly with an active Slack community. 

3. **Reliability**: GPUs of all kind from A10 to A100 are available. Not only that they provide lot of good ways of handling batched inference and supports concurrent requests with multiple workers. You can check out more on their [documentation](https://modal.com/docs/examples)