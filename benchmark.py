import os 
import requests
from typing import Union, List

# service_id = "gx0098lddlsp1c"

def response(chat_query: Union[str, List[str]], service_id: str):
    runpod_api_token = os.environ.get("RUNPOD_API_TOKEN", None)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {runpod_api_token}",
    }

    url = f"https://api.runpod.ai/v2/{service_id}/run"
    data_to_send = {
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

    # First post this request and you will get a Job ID in return 
    response = requests.post(url=url, headers=headers, json=data_to_send, timeout=600,)
    
    # Now use this ID to /stream results untill the /status shows COMPLETE
    job_id = response.json()["id"]
    url = f"https://api.runpod.ai/v2/{service_id}/stream/{job_id}"

    while True:
        response = requests.get(url, headers=headers)
        response = response.json()

        if response["status"] == "COMPLETED":
            break
        print(response["stream"][0]["output"])
    return


if __name__ == "__main__":
    chat_input = [
        {"role": "user", "content": "be helpful"},
        {
            "role": "assistant",
            "content": "I'm doing great. How can I help you today?",
        },
        {
            "role": "user",
            "content": "I'd like to show off how chat templating works!",
        },
    ]

    response(chat_query=chat_input, service_id="gx0098lddlsp1c")
