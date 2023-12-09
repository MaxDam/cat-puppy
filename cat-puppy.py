from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel, Field
from typing import Dict
from cat.log import log
from .puppy import Puppy


class MySettings(BaseModel):
    base_url: str = Field(
        title="base url",
        default="http://host.docker.internal:11434"
    )
    model: str = Field(
        title="model",
        default="zephyr:7b-beta"  #openchat
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
        default=0.1
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


@hook()
def agent_fast_reply(fast_reply, cat) -> Dict:
    
    # If the cat doesn't call any tools, call puppy
    num_procedural_mems = len( cat.working_memory["procedural_memories"] )
    log.warning(f"Number procedural memories: {num_procedural_mems}")
    if num_procedural_mems == 0:

        # Get puppy
        puppy = get_puppy(cat)

        # Get user message
        user_message = cat.working_memory["user_message_json"]["text"]

        # Call puppy llm
        log.warning(f"Calling puppy llm: {user_message}")
        response = puppy.llm(user_message, stream=True)
        log.warning(f"received response in: {puppy.last_response_time}")
        return { "output": response } 
    
    return fast_reply


# Return puppy llm
def get_puppy(cat):
    # load puppy llm only fist time
    if "puppy_llm" not in cat.working_memory.keys():
        log.warning(f"Load putty llm.. ")
        puppy = Puppy(cat)
        cat.working_memory["puppy_llm"] = puppy

    return cat.working_memory["puppy_llm"]
