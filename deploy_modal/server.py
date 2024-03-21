import json
from typing import Union, List
from pydantic import BaseModel, Field
from fastapi.responses import StreamingResponse
from modal import web_endpoint

# Define the required things for building the server
from engine import stub, HFEngine, HF_DOCKER_IMAGE
from constants import KEEP_WARM, NUM_CONCURRENT_REQUESTS, TIMEOUT


class JobInput(BaseModel):
    messages: Union[str, List[dict]]
    max_new_tokens: int | None = Field(default=512)
    temperature: float | None = Field(default=0.7)
    top_p: float | None = Field(default=0.95)


@stub.function(
    keep_warm=KEEP_WARM,
    allow_concurrent_inputs=NUM_CONCURRENT_REQUESTS,
    timeout=TIMEOUT,
    image=HF_DOCKER_IMAGE,
)
@web_endpoint(method="POST", label="completion")
async def completion(item: JobInput):
    model = HFEngine()
    gen_kwargs = {
        "max_new_tokens": item.max_new_tokens,
        "temperature": item.temperature,
        "top_p": item.top_p,
        "do_sample": True,
    }

    async def _stream_completion():
        async for text in model.stream.remote_gen.aio(
            chat_input=item.messages, generation_kwargs=gen_kwargs
        ):
            yield f"data: {json.dumps(dict(text=text), ensure_ascii=False)}\n\n"

    return StreamingResponse(
        _stream_completion(), media_type="text/event-stream"
    )
