import os
import time
import json
import argparse
import tiktoken
import requests
from dotenv import load_dotenv
from typing import Union, List, Optional

def get_response_from_service(
    url: str,
    chat_query: Union[str, List[dict]],
    service: str,
    run_pod_service_id: Optional[str] = None,
):
    assert service in ["modal", "beam", "runpod"], ValueError(
        "Benchmark is available for services: 'modal', 'runpod', and 'beam'"
    )

    load_dotenv()

    if service == "beam" and url.split("/")[-1] != "stream":
        url = f"{url}/stream"

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
                extracted_text = response["stream"][0]["output"]
                response += extracted_text
                print(extracted_text)
        else:
            for text in completion_response.iter_lines():
                decoded_string = text.decode("utf-8")
                if len(decoded_string) > 0:
                    json_string = decoded_string.split(":", 1)[1].strip()
                    data_dict = json.loads(json_string)
                    extracted_text = data_dict["text"]
                    print(extracted_text)
                    response = response + extracted_text
        end_time = time.time() - start
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokens = encoding.encode(response, disallowed_special=())
        tokens_per_second = len(tokens) / end_time

        results = {
            "service": service,
            "runpod_service_id": run_pod_service_id,
            "num_tokens": len(tokens),
            "tokens_per_second": tokens_per_second,
            "latency": end_time,
            "response": response,
        }
    
    print(
        "="*10,
        "Additional numbers",
    )

    for k, v in results.items():
        print(f"{k} : {v}")
        print()

    print("="*10)

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
        "--prompt", type=str, help="Prompt to get response", default="This is a test prompt"
    )

    parser.add_argument(
        "--runpod_id", type=str, help="Specific to runpod deployment, the service id to invoke streaming of tokens"
    )

    args = parser.parse_args()
    get_response_from_service(
        service=args.service,
        url=args.url,
        chat_query=args.prompt,
        run_pod_service_id=args.runpod_id
    )