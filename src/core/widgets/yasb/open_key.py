import os
import re

import win32con
import win32gui
from PyQt6.QtWidgets import QLabel

from core.validation.widgets.yasb.open_key import OpenKeyConfig
from core.widgets.base import BaseWidget


class OpenKeyWidget(BaseWidget):
    validation_schema = OpenKeyConfig

    OP_TOGGLE = 69420
    OP_GET = 69421
    OP_CONTROL_PANEL = 69422

    EN = 69
    VN = 72

    def __init__(self, config: OpenKeyConfig):
        super().__init__(config.update_interval, class_name=f"openkey-widget {config.class_name}")
        self.config = config

        self._init_container()
        self.build_widget_label(config.label, label_placeholder="Loading...")

        self.register_callback("update_label", self._update_label)
        self.register_callback("toggle_im", self.toggle_im)
        self.register_callback("toggle_control_panel", self.toggle_control_panel)

        self.callback_left = config.callbacks.on_left
        self.callback_middle = config.callbacks.on_middle
        self.callback_right = config.callbacks.on_right
        self.callback_timer = "update_label"

        self.start_timer()

    def _update_label(self):
        language = self.get_resp(self.sig(self.OP_GET))
        label_parts = re.split(r"(<span.*?>.*?</span>)", self.config.label)
        widget_index = 0

        for part in label_parts:
            part = part.strip()
            if not part or widget_index >= len(self._widgets):
                continue

            widget = self._widgets[widget_index]
            if not isinstance(widget, QLabel):
                continue

            if "<span" in part and "</span>" in part:
                widget.setText(re.sub(r"<span.*?>|</span>", "", part).strip())
            else:
                widget.setText(part.replace("%l", language))
            widget.show()
            widget_index += 1

    @staticmethod
    def get_resp(resp: int) -> str:
        if resp == OpenKeyWidget.EN:
            return os.environ.get("OKC_EN", "EN")
        if resp == OpenKeyWidget.VN:
            return os.environ.get("OKC_VN", "VN")
        return "process communication error"

    @staticmethod
    def sig(signum: int) -> int:
        previous_instance = win32gui.FindWindow("OpenKeyVietnameseInputMethod", None)
        if previous_instance:
            return win32gui.SendMessage(previous_instance, win32con.WM_USER + signum, 0, 0)
        return -1

    def toggle_im(self):
        self.sig(self.OP_TOGGLE)

    def toggle_control_panel(self):
        self.sig(self.OP_CONTROL_PANEL)
