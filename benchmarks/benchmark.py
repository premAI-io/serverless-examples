import os
import time
import json
import logging
import argparse
import tiktoken
import requests
from tqdm import tqdm
from dotenv import load_dotenv
from typing import Union, List, Optional


def log_and_print(logger, string):
    logger.info(string)
    print(string)


def get_single_response_benchmark(
    url: str,
    chat_query: Union[str, List[dict]],
    service: str,
    run_pod_service_id: Optional[str] = None,
):
    assert service in ["modal", "beam", "runpod"], ValueError(
        "Benchmark is available for services: 'modal', 'runpod', and 'beam'"
    )

    load_dotenv()

    if service == "modal":
        headers = {"Content-Type": "application/json"}
    else:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": (
                f'Basic {os.environ.get("BEAM_API_KEY")}'
                if service == "beam"
                else f'Bearer {os.environ.get("RUNPOD_API_KEY")}'
            ),
        }

    if service in ["modal", "beam"]:
        input_data = {
            "messages": chat_query,
            "temperature": 0.1,
            "top_p": 0.7,
            "max_new_tokens": 512,
        }
    else:
        input_data = {
            "input": {
                "messages": chat_query,
                "stream": True,
                "sampling_params": {
                    "temperature": 0.1,
                    "top_p": 0.7,
                    "max_new_tokens": 512,
                },
            }
        }

    start = time.time()
    stream = True if service != "runpod" else False
    completion_response = requests.post(
        url=url, headers=headers, json=input_data, timeout=600, stream=stream
    )

    if completion_response.status_code == 200:
        response = ""
        if service == "runpod":
            job_id = completion_response.json()["id"]
            url = (
                f"https://api.runpod.ai/v2/{run_pod_service_id}/stream/{job_id}"
            )

            while True:
                response = requests.get(url, headers=headers)
                response = response.json()
                if response["status"] == "COMPLETED":
                    break
                response += response["stream"][0]["output"]
        else:
            for text in completion_response.iter_lines():
                decoded_string = text.decode("utf-8")
                if len(decoded_string) > 0:
                    json_string = decoded_string.split(":", 1)[1].strip()
                    data_dict = json.loads(json_string)
                    extracted_text = data_dict["text"]
                    response = response + extracted_text
        end_time = time.time() - start
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokens = encoding.encode(response, disallowed_special=())
        tokens_per_second = len(tokens) / end_time

        return {
            "service": service,
            "runpod_service_id": run_pod_service_id,
            "num_tokens": len(tokens),
            "tokens_per_second": tokens_per_second,
            "latency": end_time,
            "response": response,
        }

    return None


def perform_benchmark(service: str, url: str, run_pod_service_id: Optional[str] = None):
    all_prompts = json.load(open("benchmarks/questions.json", "r"))["questions"]
    coldstart_prompts = all_prompts[:3]
    remaining_prompts = all_prompts[5:]
    coldstart_avg, avg = 0.0, 0.0

    logger = logging.getLogger(__name__)
    log_and_print(
        logger, "=============== COLDSTART BENCHMARK ===============\n"
    )

    for prompt in tqdm(coldstart_prompts, total=3):
        results = get_single_response_benchmark(
            chat_query=prompt, service=service, url=url, run_pod_service_id=run_pod_service_id
        )
        if results is not None:
            logger.info(
                (
                    f"Completion test for service: {service} for completed successfully. "
                    f"Number of tokens: {results['num_tokens']}. "
                    f"Tokens per second: {results['tokens_per_second']}. "
                    f"Time: {results['latency']} seconds."
                )
            )
            coldstart_avg += results["latency"]

    log_and_print(
        logger, "=============== AFTER COLDSTART BENCHMARK ===============\n"
    )

    for prompt in tqdm(remaining_prompts, total=27):
        results = get_single_response_benchmark(
            chat_query=prompt, service=service, url=url
        )
        if results is not None:
            logger.info(
                (
                    f"Completion test for service: {service} for completed successfully. "
                    f"Number of tokens: {results['num_tokens']}. "
                    f"Tokens per second: {results['tokens_per_second']}. "
                    f"Time: {results['latency']} seconds."
                )
            )
            avg += results["latency"]

    log_and_print(
        logger,
        f"Average latency for coldstart: {(coldstart_avg / len(coldstart_prompts))} seconds and after this average remains: {(avg / len(remaining_prompts))} seconds",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test generate function")
    parser.add_argument(
        "service",
        type=str,
        help="Which service to benchmark. Options: 'modal', 'beam' and 'runpod'",
    )
    parser.add_argument(
        "--url", type=str, help="Base URL of the deployed model"
    )

    parser.add_argument(
        "--name", type=str, help="The name of the experiment you want to track", default="def-experiment"
    )

    parser.add_argument(
        "--runpod_id", type=str, help="Specific to runpod deployment, the service id to invoke streaming of tokens"
    )

    args = parser.parse_args()

    logging.basicConfig(
        filename=f"Logs/{args.name}.log",
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )

    perform_benchmark(service=args.service, url=args.url, run_pod_service_id=args.runpod_id)
