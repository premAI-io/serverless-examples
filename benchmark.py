import json
import requests
from typing import Union, List

def benchmark_response(chat_query: Union[str, List[str]], service: str):
    assert service in ["modal", "beam", "runpod"], ValueError("Benchmark is available for services: 'modal', 'runpod', and 'beam'")
    headers = {
        "Content-Type": "application/json",
        'Authorization': 'Bearer H2JVX2OP30OM5WW1Y4YCC13T3GVG4Q25SBYZ56OS',
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
        }, "https://api.runpod.ai/v2/gx0098lddlsp1c/run")
    }
    response = requests.post(
        url=data_and_url_mapping[service][1], 
        headers=headers, json=data_and_url_mapping[service][0], timeout=600,
    )
    
    job_id = response.json()['id']
    url = f'https://api.runpod.ai/v2/gx0098lddlsp1c/stream/{job_id}'

    while True:
        response = requests.get(url, headers=headers)
        response = response.json()

        if response['status'] == 'COMPLETED':
            break

        print(response['stream'][0]['output'])

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