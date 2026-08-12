from pydantic import Field

from core.validation.widgets.base_model import (
    CallbacksConfig,
    CustomBaseModel,
    KeybindingConfig,
)


class OpenKeyCallbacksConfig(CallbacksConfig):
    on_left: str = "toggle_im"
    on_right: str = "toggle_control_panel"


class OpenKeyConfig(CustomBaseModel):
    label: str = "IM: %l"
    update_interval: int = Field(default=50, ge=0, le=60000)
    class_name: str = ""
    keybindings: list[KeybindingConfig] = []
    callbacks: OpenKeyCallbacksConfig = OpenKeyCallbacksConfig()
