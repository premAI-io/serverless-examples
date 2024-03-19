import asyncio
from queue import Empty
from modal import method, enter, exit 
from typing import Union, List 

class HFEngine:
    @enter()
    def start_engine(self):
        from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer

        # Please note: defining the imports inside the methods seems to be essential sometimes
        # otherwise it gives error sometimes during deployment
        # and also if imports are inisde methods this would mean that you are not required to install these additional
        # libraries in your local other than modal 
        
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name_or_path, trust_remote_code=True).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path, trust_remote_code=True)
        self.streamer = TextIteratorStreamer(self.tokenizer)
        return self
    
    @exit()
    def terminate_engine(self):
        import gc 
        import torch

        del self.model
        torch.cuda.synchronize()
        gc.collect()
    
    @method()
    async def stream(self, chat_input: Union[str, List[dict]], generation_kwargs: dict):
        from threading import Thread

        if isinstance(chat_input, str):
            chat_input = [{"role": "user", "content": chat_input}]
        input_ids = self.tokenizer.apply_chat_template(
            conversation=chat_input, tokenize=True, return_tensors="pt"
        ).to(self.device)

        gen_kwargs = dict(
            input_ids=input_ids,
            streamer=self.streamer,
            **generation_kwargs
        )

        thread = Thread(target=self.model.generate, kwargs=gen_kwargs)
        thread.start()

        for next_token in self.streamer:
            try:
                if next_token is not None:
                    yield next_token
            except Empty:
                await asyncio.sleep(0.001) 