from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import Dict, Optional
from cat.log import log

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama


class MySettings(BaseModel):
    base_url: "http://host.docker.internal:11434"
    model: str = "openchat"
    num_ctx: int = 2048
    repeat_last_n: int = 64
    repeat_penalty: float = 1.1
    temperature: float = 0.8


@plugin
def settings_schema():   
    return MySettings.schema()


# Hook the main prompt prefix
@hook(priority=1)
def agent_prompt_prefix(prefix, cat) -> str:
    return prefix


# Called after cat bootstrap
@hook(priority=1)
def after_cat_bootstrap(cat):
    
    # Get settings
    settings = cat.mad_hatter.plugins["my_plugin_name"].load_settings()

    # initialize puppy llm and save it into working memory
    try:
        puppy_llm = Ollama.default(**settings)
        cat.working_memory["PUPPY-LLM"] = puppy_llm
    except Exception  as e:
        print(f"There was an error in puppy llm initialization: {e}")
    
    '''
    # initialize puppy llm and save it into working memory
    puppy_llm = Ollama(
        model="openchat",
        verbose=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )
    cat.working_memory["puppy_llm"] = puppy_llm
    '''
    pass


@hook(priority=1)
def agent_fast_reply(fast_reply, cat) -> Dict:
    
    return_direct = False

    # If the cat doesn't call any tools ..
    num_procedural_mems = len( cat.working_memory["procedural_memories"] )
    if num_procedural_mems == 0 and "puppy_llm" in cat.working_memory.keys():

        # Get the puppy llm from working memory
        puppy_llm = cat.working_memory["puppy_llm"]

        # Get user message
        user_message = cat.working_memory["user_message_json"]["text"]

        # Call puppy llm
        response = puppy_llm(user_message)
        return_direct = True
    

    if return_direct:
        fast_reply = { "output": response }
        
    return fast_reply
