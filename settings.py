from typing import Optional
from pydantic import BaseModel, Field

from cat.mad_hatter.decorators import plugin


class MySettings(BaseModel):
    base_url: str = Field(
        title="base url",
        default="http://host.docker.internal:11434"
    )
    model: str = Field(
        title="model",
        default="zephyr:7b-beta"  # openchat
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
    puppy_prompt: str = Field(
        title="Puppy prompt",
        default=("You are the Cheshire Cat's pet," +
                 "an intelligent artificial intelligence that runs locally on the user's PC. " +
                 "Respond to the Human using very short, precise sentences, focusing on the subsequent context. " +
                 "Just reply without reporting the entire previous conversation."),
        extra={"type": "TextArea"}
    )
    use_by_default: bool = Field(
        title="use puppy by default",
        default=True
    )
    use_for_start_tools: bool = Field(
        title="use for start tools",
        default=False
    )
    sentence_max_length: Optional[int] = Field(
        title="sentence max length",
        default=None
    )


@plugin
def settings_schema():
    return MySettings.schema()
