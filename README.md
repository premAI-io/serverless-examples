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

## 🧐 Analysis and Results 

In this section we are going to analyse some benchmarks and some overall thoughts while building the application. 

### Modal
Before proceeding to the analysis, if you want to reproduce the results, you need to first start the modal server. Instruction available [here](/modal/README.md). After this you need to run the benchmark file. Make sure to stay under this project root folder. 

```bash
python benchmarks/benchmark.py modal --base_url https://premai-io--completion-dev.modal.run
```
Change the `--base_url` with the one generated from your deployement using Modal. Now let's discuss the results. 

1. **Costs:** 
    - `Stable LM deployement on A10G:` The approx cost that took for the experiment in an A10G-32 GB for 30 prompts (3 during Cold Start and 27 after that) was around 0.12 $. When it comes to latency, the average cold start latency was around 12.98 ms and after that average latency was around 11.08 ms. 

    - `Mistral 7B Instruct deployement on A100:` The approx cost that took for the experiment in an A100-80 GB for 30 prompts (3 during Cold Start and 27 after that) was around 0.7 $. When it comes to latency, the average cold start latency was around 24.8 ms and after that average latency was around 14.45 ms. So roughly it takes ~ 10 seconds to get the server ready before it takes the first request. 

2. **Quality/Level of Abstraction**: When it comes to Modal, it is super easy to start deploying your model of choice. It gives a nice abstractions on creating docker files through their python interfaces. However, when it comes to huge amount of customisation (from ground up), users might have to go through the documentation more to understand nuances associated with the abstract which could be a potential tradeoff with low level customization. But Modal seems to be super developer friendly with an active Slack community. 

3. **Reliability**: GPUs of all kind from A10 to A100 are available. Not only that they provide lot of good ways of handling batched inference and supports concurrent requests with multiple workers. You can check out more on their [documentation](https://modal.com/docs/examples)

### Beam Cloud
Before proceeding to the analysis, if you want to reproduce the results, you need to first start the Beam's server. Instruction available [here](/beam-exp/README.md). After this you need to run the benchmark file. Make sure to stay under this project root folder. Before runnning, please export your API KEY in the env variable or put it inside the `.env` file under root folder, like this:

```bash
BEAM_API_KEY="BEAM-key"
```
After this, you are ready and now you can run the benchmarks for beam like this:

```bash
python benchmarks/benchmark.py beam --base_url <generated-url>/stream
```
Once you deployed/served the model in Beam, it will give you an url. You need to copy that url and append a `/stream` route to enable benchmarking for Beam. Here is an example:

```bash
python3 benchmarks/benchmark.py beam --base_url https://fpi3j-65f55bb04b5f2400249a4fbf.apps.beam.cloud/stream
```

> The experiment that we did for the case with Beam is using `A10G` GPU and the model used for deploying is: `stabilityai/stablelm-zephyr-3b`. 

1. **Costs:** The approx cost that took for the experiment in an A100-80 GB for 30 prompts (3 during Cold Start and 27 after that) was around 0.05604 $. When it comes to latency, the average cold start latency was around `13.0020 ms` and after that average latency was around `12.76 ms`. So roughly it takes ~ 11 seconds to get the server ready before it takes the first request. 

2. **Quality/Level of Abstraction**: Beam is also easier to get started. But they do not have very good documentation. This makes the developing process take much more time than expected when doing customization. 

3. **Reliability**: A100 GPUs are not readily available. You have to mail Beam in order to get access. Although Beam provides nice post production visualizations showing loads, cold starts, billing amount, any spikes etc. But it is still in super early stage. 