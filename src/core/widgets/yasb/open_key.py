import os

from core.widgets.base import BaseWidget
from core.validation.widgets.yasb.open_key import VALIDATION_SCHEMA
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt
import win32gui
import win32con


class OpenKeyWidget(BaseWidget):
    validation_schema = VALIDATION_SCHEMA

    OP_TOGGLE = 69420
    OP_GET = 69421
    OP_CONTROL_PANEL = 69422

    EN = 69
    VN = 72

    def __init__(
            self,
            label: str,
            update_interval: int,
            callbacks: dict[str, str],
    ):
        super().__init__(update_interval, class_name="openkey-widget")
        self._label = label
        self._update_interval = update_interval
        self._callbacks = callbacks

        # Construct container
        self._widget_container_layout: QHBoxLayout = QHBoxLayout()
        self._widget_container_layout.setSpacing(0)
        self._widget_container_layout.setContentsMargins(0, 0, 0, 0)
        # Initialize container
        self._widget_container: QWidget = QWidget()
        self._widget_container.setLayout(self._widget_container_layout)
        self._widget_container.setProperty("class", "widget-container")
        # Add the container to the main widget layout
        self.widget_layout.addWidget(self._widget_container)

        # self.register_callback("toggle_label", self._toggle_label)
        self.register_callback("update_label", self._update_label)
        self.register_callback("toggle_im", self.toggle_im)
        self.register_callback("toggle_control_panel", self.toggle_control_panel)

        self.callback_left = callbacks['on_left']
        self.callback_right = callbacks['on_right']
        self.callback_middle = callbacks['on_middle']
        self.callback_timer = "update_label"

        self._widgets = []

        obj = QLabel('text lel')
        obj.setProperty("class", "label")
        obj.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._widget_container_layout.addWidget(obj)
        self._widgets.append(obj)

        self._update_label()
        self.start_timer()

    @staticmethod
    def get_en_text():
        if 'OKC_EN' in os.environ:
            return str(os.environ['OKC_EN'])
        return 'EN'

    @staticmethod
    def get_vn_text():
        if 'OKC_VN' in os.environ:
            return str(os.environ['OKC_VN'])
        return 'VN'

    @staticmethod
    def get_resp(resp):
        if resp == OpenKeyWidget.EN:
            return OpenKeyWidget.get_en_text()
        elif resp == OpenKeyWidget.VN:
            return OpenKeyWidget.get_vn_text()
        else:
            return 'process communication error'

    @staticmethod
    def sig(signum):
        previous_instance = win32gui.FindWindow("OpenKeyVietnameseInputMethod", None)
        if previous_instance:
            result = win32gui.SendMessage(previous_instance, win32con.WM_USER + signum, 0, 0)
            return result
        else:
            return -1

    def _update_label(self):
        active_widgets = self._widgets
        text = self.get_resp(self.sig(self.OP_GET))
        active_widgets[0].setText(self._label.replace('%l', text))

    def toggle_im(self):
        self.sig(self.OP_TOGGLE)

    def toggle_control_panel(self):
        self.sig(self.OP_CONTROL_PANEL)