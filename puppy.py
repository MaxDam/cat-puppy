from langchain.llms import Ollama
from cat.log import log
from cat.looking_glass.callbacks import NewTokenHandler
import copy
import time

class Puppy:

    def __init__(self, cat):
        self.cat = cat
        self.last_response_time = 0

        # Get all settings
        self.settings = cat.mad_hatter.get_plugin().load_settings()
        
        # Get only setting for llm puppy
        llm_settings = copy.copy(self.settings)
        if "streaming" in llm_settings:
            del llm_settings["streaming"]

        self.puppy_llm = Ollama(**llm_settings)


    def llm(self, prompt: str, stream: bool = False) -> str:
        
        callbacks = []
        if stream:
            callbacks.append(NewTokenHandler(self.cat))
        
        start_time = time.time()
        response = self.puppy_llm(prompt, callbacks=callbacks)
        self.last_response_time = time.time() - start_time
        return response
