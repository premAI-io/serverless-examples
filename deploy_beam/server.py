import json 
import asyncio
from queue import Empty
from threading import Thread
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
from fastapi import Request
from beam import App, Runtime, Image, Volume, RequestLatencyAutoscaler
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer

# Import from constants
from constants import NAME, CPU, GPU, PYTHON_VERSION, PACKAGES, CACHE_PATH, MODEL_ID

app = App(
    name=NAME,
    runtime=Runtime(
        cpu=CPU,
        gpu=GPU,
        image=Image(
            python_version=PYTHON_VERSION,
            python_packages=PACKAGES
        ),
    ),
    # Storage Volume for model weights
    volumes=[Volume(name="cached_models", path=CACHE_PATH)],
)

# Autoscale by request latency
autoscaler = RequestLatencyAutoscaler(desired_latency=30, max_replicas=5)

def load_models():
    # this is a one time function which beam uses when the server starts for the
    # very first time. After that, it loads the model from cache dir

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        cache_dir=CACHE_PATH, 
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID, 
        cache_dir=CACHE_PATH
    )

    streamer = TextIteratorStreamer(tokenizer=tokenizer)
    return model, tokenizer, streamer


# We create a simple FastAPI application with streaming responses 

@app.asgi(workers=2, authorized=False, loader=load_models)
def web_server(**inputs):
    app_server = FastAPI()
    
    async def _stream(chat_input: str, generation_kwargs: dict) -> AsyncGenerator[str, None]:
        model, tokenizer, streamer = inputs["context"]
        if isinstance(chat_input, str):
            chat_input = [{"role": "user", "content": chat_input}]

        print(chat_input)

        input_ids = tokenizer.apply_chat_template(
            conversation=chat_input, tokenize=True, return_tensors="pt"
        ).to("cuda")

        gen_kwargs = dict(
            input_ids=input_ids,
            streamer=streamer,
            **generation_kwargs
        )

        thread = Thread(target=model.generate, kwargs=gen_kwargs)
        thread.start()

        for chunk in streamer:
            try:
                if chunk is not None:
                    print(chunk)
                    yield chunk
            except Empty:
                await asyncio.sleep(0.001)
    
    @app_server.post("/stream")
    async def stream_response(request: Request):
        data = await request.json()
        prompt = data.get("messages", "")
        generation_kwargs = dict(
            max_new_tokens = int(data.get("max_new_tokens", 512)),
            temperature = float(data.get("temperature", 0.1)),
            top_p = float(data.get("top_p", 0.95)),
        )        

        print(prompt)
        print(generation_kwargs)

        async def stream_gen():
            async for chunk in _stream(chat_input=prompt, generation_kwargs=generation_kwargs):
                yield f"data: {json.dumps(dict(text=chunk), ensure_ascii=False)}\n\n"
        return StreamingResponse(stream_gen(), media_type="text/event-stream")
    
    return app_server
