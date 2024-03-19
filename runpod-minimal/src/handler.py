import asyncio
import runpod 

class JobInput:
    def __init__(self, job):
        self.llm_input = job.get("messages")
        self.stream = job.get("stream", False)
        self.sampling_params = job.get(
            "sampling_params", {
                "temperature": 0.1,
                "top_p": 0.7,
                "max_new_tokens":512
            }
        )

async def handler(job):
    job_input = JobInput(job["input"])
    print(job_input)
    for count in range(10):
        result = f"This is the {count} generated output."
        yield result
        await asyncio.sleep(5)

runpod.serverless.start(
    {
        "handler": handler,
    }
)