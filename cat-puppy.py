from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import Dict, Optional
from cat.log import log

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama


class MySettings(BaseModel):
    required_int: int
    optional_int: int = 69
    required_str: str
    optional_str: str = "meow"
    required_date: date
    optional_date: date = 1679616000

    #base_url: "http://host.docker.internal:11434"
    #model: str = "openchat"
    #num_ctx: int = 2048
    #repeat_last_n: int = 64
    #repeat_penalty: float = 1.1
    #temperature: float = 0.8

@plugin
def settings_schema():   
    return MySettings.schema()

@tool
def get_the_day(tool_input, cat):
    """Get the day of the week. Input is always None."""

    dt = datetime.now()

    return dt.strftime('%A')

@hook
def before_cat_sends_message(message, cat):

    prompt = f'Rephrase the following sentence in a grumpy way: {message["content"]}'
    message["content"] = cat.llm(prompt)

    return message


@hook(priority=0)
def before_cat_bootstrap(cat):
    """Hook into the Cat start up.

    Bootstrapping is the process of loading the plugins, the natural language objects (e.g. the LLM),
    the memories, the *Agent Manager* and the *Rabbit Hole*.

    This hook allows to intercept such process and is executed in the middle of plugins and
    natural language objects loading.

    This hook can be used to set or store variables to be propagated to subsequent loaded objects.

    Parameters
    ----------
    cat : CheshireCat
        Cheshire Cat instance.
    """
    pass # do nothing


# Called after cat bootstrap
@hook(priority=0)
def after_cat_bootstrap(cat):
    """Hook into the end of the Cat start up.

    Bootstrapping is the process of loading the plugins, the natural language objects (e.g. the LLM),
    the memories, the *Agent Manager* and the *Rabbit Hole*.

    This hook allows to intercept the end of such process and is executed right after the Cat has finished loading
    its components.

    This can be used to set or store variables to be shared further in the pipeline.

    Parameters
    ----------
    cat : CheshireCat
        Cheshire Cat instance.
    """

    puppy_llm = Ollama(
        model="openchat",
        verbose=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )
    response = puppy_llm("Tell me very briefly about world war II")
    cat.working_memory["PUPPY-LLM"] = puppy_llm

    pass # do nothing


@hook(priority=0)
def agent_fast_reply(fast_reply, cat) -> Dict:
    """This hook is useful to shortcut the Cat response.
    If you do not want the agent to run, return the final response from here and it will end up in the chat without the agent being executed.

    Parameters
    --------
    fast_reply: dict
        Input is dict (initially empty), which can be enriched whith an "output" key with the shortcut response.
    cat : CheshireCat
        Cheshire Cat instance.

    Returns
    --------
    response : Union[None, Dict]
        Cat response if you want to avoid using the agent, or None / {} if you want the agent to be executed.
        See below for examples of Cat response

    Examples
    --------

    Example 1: can't talk about this topic
    ```python
    # here you could use cat._llm to do topic evaluation
    if "dog" in agent_input["input"]:
        return {
            "output": "You went out of topic. Can't talk about dog."
        }
    ```

    Example 2: don't remember (no uploaded documents about topic)
    ```python
    num_declarative_memories = len( cat.working_memory["declarative_memories"] )
    if num_declarative_memories == 0:
        return {
           "output": "Sorry, I have no memories about that."
        }
    ```
    """

    return_direct = True
    response = "my response"

    if return_direct:
        fast_reply = { "output": response }
        
    return fast_reply