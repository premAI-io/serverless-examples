# Define the model name and model dir
MODEL_DIR = "/model"
BASE_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"


# Name the stub (it should all be in lower case)
STUB_NAME = f"{BASE_MODEL.lower()}-deployement"

### Server level default configs
# Keep warm: is the warm pool size or the minimum number of containers that will always be up for your serverless function to get executed (Modal will scale up more containers from there based on need or demand)

KEEP_WARM = 1

# num of concurrent requests: is the number of concurrent requests a container should handle
NUM_CONCURRENT_REQUESTS = 10

# timeout: This is the server timeout after which it would be shutdown the server.
TIMEOUT = 600

# Number of GPUs to use
GPU_COUNT = 1
