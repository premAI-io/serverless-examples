import json
import requests
from typing import Union, List

def benchmark_response(chat_query: Union[str, List[str]], service: str):
    assert service in ["modal", "beam", "runpod"], ValueError("Benchmark is available for services: 'modal', 'runpod', and 'beam'")
    headers = {
        "Content-Type": "application/json"
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
        }, "http://localhost:8000/run")
    }
    response = requests.post(
        url=data_and_url_mapping[service][1], 
        headers=headers, json=data_and_url_mapping[service][0], timeout=600,
    )
    
    job_id = response.json()['id']
    print(job_id)
    url = f'http://localhost:8000/stream/{job_id}'

    while True:
        get_status = requests.get(url, headers=headers)
        print(get_status.text)
        import time
        time.sleep(2)

    return
    response = requests.post(
        url=url,
        headers=headers,
    )
    print(response.status_code)

    if response.status_code == 200:
        for i, res in enumerate(response.iter_lines()):
            print(i, res)
    return
    
    if response.status_code == 200:
        for i, res in enumerate(response.iter_lines()):
            print(i, res)

if __name__ == '__main__':
    chat_input = [
        {"role": "user", "content": "be helpful"},
        {"role": "assistant", "content": "I'm doing great. How can I help you today?"},
        {"role": "user", "content": "I'd like to show off how chat templating works!"},
    ] 

    benchmark_response(chat_query=chat_input, service="runpod")