from langchain.llms import Ollama
from cat.log import log
from cat.looking_glass.callbacks import NewTokenHandler
from cat.looking_glass.prompts import MAIN_PROMPT_PREFIX, MAIN_PROMPT_SUFFIX

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


    # Invoke puppy LLM 
    def llm(self, prompt: str, stream: bool = False) -> str:
        
        # Obtain the prompt with context
        prompt = self._get_full_prompt(prompt)
        print("prompt:\n{prompt}")

        # Get Callback for streaming
        callbacks = []
        if stream:
            callbacks.append(NewTokenHandler(self.cat))
        
        # Invoke Puppy LLM
        start_time = time.time()
        response = self.puppy_llm(prompt, callbacks=callbacks)
        self.last_response_time = time.time() - start_time

        return response


    # Get full prompt with context
    def _get_full_prompt(self, prompt: str):
        prompt_prefix = self.cat.mad_hatter.execute_hook("agent_prompt_prefix", MAIN_PROMPT_PREFIX, cat=self.cat)
        json_context = self.cat.agent_manager.format_agent_input(self.cat.working_memory)
        json_context['input'] = prompt
        json_context['tools_output'] = ''
        prompt_suffix = MAIN_PROMPT_SUFFIX.format(**json_context)
        prompt = prompt_prefix + "\n" + prompt_suffix
        return prompt
