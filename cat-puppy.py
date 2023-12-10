from typing import Dict

from .puppy import Puppy

from cat.log import log
from cat.mad_hatter.decorators import tool, hook, plugin


@plugin
def activate(plugin):
    log.warning(f"Plugin start")
    pass


# Hook the main prompt prefix
@hook()
def agent_prompt_prefix(prefix, cat) -> str:
    if "puppy_llm" in cat.working_memory.keys():
        puppy = cat.working_memory["puppy_llm"]
        prefix = puppy.settings["puppy_prompt"]
    return prefix


@hook()
def agent_fast_reply(fast_reply, cat) -> Dict:
    # Get puppy
    puppy = get_puppy(cat)
    
    # Invoke cat puppy hook "set cat puppy"
    try:
        cat.mad_hatter.execute_hook("set_cat_puppy", puppy, cat=cat)
    except Exception as e:
        log.warning(f"{e}")
    
    '''
    if the use_by_default property is true the component 
    decide when to use the llm puppy
    ''' 
    if puppy.settings["use_by_default"] is True:
        use_puppy = True
        
        # Check if tool is called
        num_procedural_mems = len(cat.working_memory["procedural_memories"])
        log.warning(f"Number procedural memories: {num_procedural_mems}")
        if num_procedural_mems > 0:
            if puppy.settings["use_for_start_tools"] is False:
                log.warning(f"don't use puppy because tools are called")
                use_puppy = False

        # Get user message
        user_message = puppy.cat.working_memory["user_message_json"]["text"]

        # Check sentence length
        if len(user_message) > puppy.settings["sentence_max_length"]:
            if puppy.settings["use_for_large_sentences"] is False:
                log.warning(f"don't use puppy because the sentence are too logn")
                use_puppy = False

        # If use puppy -> Call puppy llm
        if use_puppy is True:    
            log.warning(f"Calling puppy llm")
            response = puppy.llm(user_message, stream=True)
            log.warning(f"received response in: {puppy.last_response_time}")
            return {"output": response}

    '''
    if the use_by_default property is false you can implement a hook called use_cat_puppy 
    where you can decide whether or not to use the llm puppy
    '''  
    if puppy.settings["use_by_default"] is False:
        try:
            use_puppy = cat.mad_hatter.execute_hook("use_cat_puppy", puppy, cat=cat)
            if use_puppy is True:
                log.warning(f"Calling puppy llm")
                user_message = puppy.cat.working_memory["user_message_json"]["text"]
                response = puppy.llm(user_message, stream=True)
                log.warning(f"received response in: {puppy.last_response_time}")
                return {"output": response}
        except Exception as e:
            log.warning(f"{e}")


    return fast_reply


# Return puppy llm
def get_puppy(cat):
    # load puppy llm if not loaded
    if "puppy_llm" not in cat.working_memory.keys():
        log.warning(f"Load putty llm.. ")
        puppy = Puppy(cat)
        cat.working_memory["puppy_llm"] = puppy
    else:  # if loaded, check if settings changed
        puppy = cat.working_memory["puppy_llm"]
        settings = cat.mad_hatter.get_plugin().load_settings()
        if puppy.settings != settings:
            log.warning(f"Reload putty llm.. ")
            puppy = Puppy(cat)
            cat.working_memory["puppy_llm"] = puppy

    return puppy




################# CAT PUPPY HOOKS #################

@hook()
def set_cat_puppy(prefix, puppy, cat):
    pass


@hook()
def use_cat_puppy(prefix, puppy, cat):
    return False
