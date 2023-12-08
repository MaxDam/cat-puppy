from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Dict, Optional
from cat.log import log
from langchain.llms import Ollama
import time


class MySettings(BaseModel):
    base_url: str = Field(
        title="base url",
        default="http://host.docker.internal:11434"
    )
    model: str = Field(
        title="model",
        default="openchat"
    )
    num_ctx: int = Field(
        title="num ctx",
        default=2048
    )
    repeat_last_n: int = Field(
        title="repeat last n",
        default=64
    )
    repeat_penalty: float = Field(
        title="repeat penalty",
        default=1.1
    )
    temperature: float = Field(
        title="temperature",
        default=0.8
    )


@plugin
def settings_schema():   
    return MySettings.schema()


@plugin
def activate(plugin):
    log.warning(f"Plugin start")
    pass


# Hook the main prompt prefix
@hook()
def agent_prompt_prefix(prefix, cat) -> str:
    return prefix


# Called after cat bootstrap
@hook()
def after_cat_bootstrap(cat):
    del cat.working_memory["puppy_llm"]


# load puppy llm
def load_puppy_llm(cat):
    
    # Get settings
    settings = cat.mad_hatter.get_plugin().load_settings()
    
    # initialize puppy llm and save it into working memory
    log.warning(f"Configuring putty llm.. ")
    try:
        puppy_llm = Ollama(**settings)
        cat.working_memory["puppy_llm"] = puppy_llm
        log.warning(f"The model had been configured: {settings}")
    except Exception  as e:
        log.error(f"There was an error in puppy llm initialization: {e}")


@hook()
def agent_fast_reply(fast_reply, cat) -> Dict:
    
    return_direct = False

    # load puppy llm only fist time
    if "puppy_llm" not in cat.working_memory.keys():
        load_puppy_llm(cat)

    # If the cat doesn't call any tools ..
    num_procedural_mems = len( cat.working_memory["procedural_memories"] )
    log.warning(f"Number procedural memories: {num_procedural_mems}")
    if num_procedural_mems == 0:

        # Get the puppy llm from working memory
        puppy_llm = cat.working_memory["puppy_llm"]

        # Get user message
        user_message = cat.working_memory["user_message_json"]["text"]

        # Call puppy llm
        start_time = time.time()
        log.warning(f"Calling puppy-llm: {user_message}")
        response = puppy_llm(user_message)
        log.warning(f"received response in: {(time.time()-start_time)}")
        return_direct = True
    

    if return_direct:
        fast_reply = { "output": response }
        
    return fast_reply
