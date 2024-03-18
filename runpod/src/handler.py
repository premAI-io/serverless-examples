import runpod
from engine import HFEngine
from constants import DEFAULT_MAX_CONCURRENCY
import asyncio

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
    # engine = HFEngine()
    # job_input = JobInput(job["input"])
    # print(job_input)
    for count in range(3):
        result = f"This is the {count} generated output."
        yield result
        await asyncio.sleep(5)

    # async for delta in engine.stream(
    #     chat_input=job_input.llm_input,
    #     generation_parameters=job_input.sampling_params
    # ):
    #     yield delta 


runpod.serverless.start(
    {
        "handler": handler,
        # "return_aggregate_stream": True,
        # "concurrency_modifier": lambda x: DEFAULT_MAX_CONCURRENCY,
    }
)