import os 
import logging 
import asyncio
from dotenv import load_dotenv
from typing import List, Dict, Any, Union 
from threading import Thread 
from queue import Empty
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer

# A Basic Inference engine using HuggingFace Transformers
# In this example we are only providing method to stream responses and accept chat based input


class HFEngine:
    def __init__(self) -> None:
        load_dotenv()
        self.model, self.tokenizer, self.streamer = self._initialize_llm(
            model_name_or_path=os.environ.get("HF_MODEL_NAME"),
            tokenizer_name_or_path=os.environ.get("HF_TOKENIZER_NAME"),
            device=os.environ.get("DEVICE") or "cpu"
        )
        self.device = os.environ.get("DEVICE")

    def _initialize_llm(self, model_name_or_path: str, tokenizer_name_or_path: str, device: str):
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=model_name_or_path,
                trust_remote_code=True
            ).to(device)

            self.tokenizer = AutoTokenizer.from_pretrained(
                pretrained_model_name_or_path=tokenizer_name_or_path,
                trust_remote_code=True
            )

            self.streamer = TextIteratorStreamer(self.tokenizer)
        except Exception as error:
            logging.error("Error initializing HuggingFace engine: %s", error)
            raise error 

        return self.model, self.tokenizer, self.streamer
    
    
    async def stream(self, chat_input: Union[str, List[Dict[str, str]]], generation_parameters: Dict[str, Any]):
        try:
            async for output in self._stream(chat_input=chat_input, generation_parameters=generation_parameters):
                yield output
        except Exception as e:
            yield {"error": str(e)}
            

    async def _stream(self, chat_input: Union[str, List[Dict[str, str]]], generation_parameters: Dict[str, Any]):
        if isinstance(chat_input, str):
            chat_input = [{"user": chat_input}]
            
        input_ids = self.tokenizer.apply_chat_template(
            conversation=chat_input, tokenize=True, return_tensors="pt"
        ).to(self.device)

        generation_kwargs = dict(
            input_ids=input_ids,
            streamer=self.streamer, 
            **generation_parameters
        )
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()

        for next_token in self.streamer:
            try:
                if next_token is not None:
                    yield {"status": 200, "delta": next_token}
            except Empty:
                await asyncio.sleep(0.001) 


if __name__ == '__main__':
    engine = HFEngine()
    chat_input = [
        {"role": "user", "content": "be helpful"},
        {"role": "assistant", "content": "I'm doing great. How can I help you today?"},
        {"role": "user", "content": "I'd like to show off how chat templating works!"},
    ]

    result = engine.stream(chat_input=chat_input, generation_parameters={
        "temperature": 0.1,
        "top_p": 0.95,
        "do_sample": True, 
        "max_new_tokens": 100
    })
    
    for r in result:
        print(r)