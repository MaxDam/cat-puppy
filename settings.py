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


@plugin
def settings_schema():
    return MySettings.schema()
