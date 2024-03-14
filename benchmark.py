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
        }, "http://localhost:8000/runsync")
    }
    response = requests.post(
        url=data_and_url_mapping[service][1], 
        headers=headers, data=json.dumps(data_and_url_mapping[service][0]), timeout=600, stream=True
    )
    
    if response.status_code == 200:
        for res in response.iter_lines():
            print(res)

if __name__ == '__main__':
    chat_input = [
        {"role": "user", "content": "be helpful"},
        {"role": "assistant", "content": "I'm doing great. How can I help you today?"},
        {"role": "user", "content": "I'd like to show off how chat templating works!"},
    ] 

    benchmark_response(chat_query=chat_input, service="runpod")