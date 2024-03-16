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


def get_single_response_benchmark(chat_query: Union[str, List[dict]], service: str, url: Optional[str] = None):
    assert service in ["modal", "beam", "runpod"], ValueError("Benchmark is available for services: 'modal', 'runpod', and 'beam'")
    
    load_dotenv() 

    headers = {
        "Content-Type": "application/json"
    } if service != "beam" else {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Basic {os.environ.get("BEAM_API_KEY")}'
    }
    
    data_and_url_mapping = {
        "runpod": ({
            "input": {
                "messages": chat_query,
                "stream": True,
                "sampling_params": {
                    "temperature": 0.1,
                    "top_p": 0.7,
                    "max_new_tokens":512
                }
            }
        }, "http://localhost:8000/runsync"),

        "modal": ({
            "messages": chat_query,
            "temperature": 0.1,
            "top_p": 0.7,
            "max_new_tokens":512
        }, "https://premai-io--completion-dev.modal.run"),
        # Please change the url here

        "beam": ({
            "messages": chat_query,
            "temperature": 0.1,
            "top_p": 0.7,
            "max_new_tokens":512
        }, "https://ttjjj-65f54dc74b5f2400097b3533.apps.beam.cloud/stream")
        
    }

    
    url = data_and_url_mapping[service][1] if url is None else url 

    start = time.time()
    completion_response = requests.post(
        url=url, 
        headers=headers, data=json.dumps(data_and_url_mapping[service][0]), timeout=600, stream=True
    )

    if completion_response.status_code == 200:
        response = ""
        for text in completion_response.iter_lines():
            decoded_string = text.decode("utf-8")
            if len(decoded_string) > 0:
                json_string = decoded_string.split(":", 1)[1].strip()
                data_dict = json.loads(json_string)
                extracted_text = data_dict["text"]
                response = response + extracted_text
        
        end_time = time.time() - start
        end_time = time.time() - start
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokens = encoding.encode(response, disallowed_special=())
        number_of_tokens = len(tokens)
        tokens_per_second = number_of_tokens / end_time

        return {
            "service": service,
            "num_tokens": number_of_tokens,
            "tokens_per_second": tokens_per_second,
            "end_time": end_time
        }
    return None 

def perform_benchmark(service: str, url: Optional[str] = None):
    all_prompts = json.load(open("benchmarks/questions.json", "r"))["questions"]
    coldstart_prompts = all_prompts[:3]
    remaining_prompts = all_prompts[5:]
    coldstart_avg, avg = 0.0, 0.0

    logger = logging.getLogger(__name__)
    log_and_print(logger, "=============== COLDSTART BENCHMARK ===============\n")

    for prompt in tqdm(coldstart_prompts, total=3):
        results = get_single_response_benchmark(chat_query=prompt, service=service, url=url)
        if results is not None:  
            logger.info(
                f"Completion test for service: {service} for Mistral 7B Instruct completed successfully. "
                f"Number of tokens: {results['num_tokens']}."
                f"Tokens per second: {results['tokens_per_second']}. "
                f"Time: {results['end_time']} seconds."
            )
            coldstart_avg += results["end_time"]
        
    log_and_print(logger, "=============== AFTER COLDSTART BENCHMARK ===============\n")

    for prompt in tqdm(remaining_prompts, total=27):
        results = get_single_response_benchmark(chat_query=prompt, service=service, url=url)
        if results is not None:  
            logger.info( 
                f"Completion test for service: {service} for Mistral 7B Instruct completed successfully. "
                f"Number of tokens: {results['num_tokens']}."
                f"Tokens per second: {results['tokens_per_second']}. "
                f"Time: {results['end_time']} seconds."
            )
            avg += results["end_time"]
    
    log_and_print(
        logger,
        f"Average latency for coldstart: {(coldstart_avg / 3)} ms and after this average remains: {(avg / 27)} ms"
    )
if __name__ == '__main__':
    service = "modal"
    logging.basicConfig(
        filename=f"Logs/{service}.log",
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )

    parser = argparse.ArgumentParser(description="Test generate function")
    parser.add_argument("service", type=str, help="Which service to benchmark. Options: 'modal', 'beam' and 'runpod'")
    parser.add_argument("--base_url", type=str, help="Base URL of the deployed model")

    args = parser.parse_args()
    perform_benchmark(service=args.service, url=args.base_url)