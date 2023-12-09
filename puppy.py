from langchain.llms import Ollama
from cat.log import log
from cat.looking_glass.callbacks import NewTokenHandler
import time

class Puppy:

    def __init__(self, cat):
        self.cat = cat
        self.last_response_time = 0

        # Get settings
        settings = cat.mad_hatter.get_plugin().load_settings()
        
        if "streaming" in settings:
            del settings["streaming"]

        self.puppy_llm = Ollama(**settings)


    def llm(self, prompt: str, stream: bool = False) -> str:
        
        callbacks = []
        if stream:
            callbacks.append(NewTokenHandler(self.cat))
        
        start_time = time.time()
        response = self.puppy_llm(prompt, callbacks=callbacks)
        self.last_response_time = time.time() - start_time
        return response
