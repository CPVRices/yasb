import os

from core.widgets.base import BaseWidget
from core.validation.widgets.yasb.open_key import VALIDATION_SCHEMA
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt
import win32gui
import win32con
import re


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

        self.register_callback("update_label", self._update_label)
        self.register_callback("toggle_im", self.toggle_im)
        self.register_callback("toggle_control_panel", self.toggle_control_panel)

        self.callback_left = callbacks['on_left']
        self.callback_right = callbacks['on_right']
        self.callback_middle = callbacks['on_middle']
        self.callback_timer = "update_label"

        self._widgets = []

        self._create_dynamically_label(self._label)

        self._update_label()
        self.start_timer()

    def _create_dynamically_label(self, content: str):
        def process_content(content):
            label_parts = re.split('(<span.*?>.*?</span>)', content)
            widgets = []
            for part in label_parts:
                part = part.strip()
                if not part:
                    continue
                if '<span' in part and '</span>' in part:
                    class_name = re.search(r'class=(["\'])([^"\']+?)\1', part)
                    class_result = class_name.group(2) if class_name else 'icon'
                    icon = re.sub(r'<span.*?>|</span>', '', part).strip()
                    label = QLabel(icon)
                    label.setProperty("class", class_result)
                else:
                    label = QLabel(part)
                    label.setProperty("class", "label")
                    label.setText("Loading...")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self._widget_container_layout.addWidget(label)
                widgets.append(label)
                label.show()

            return widgets

        self._widgets = process_content(content)

    def _update_label(self):
        def get_text():
            text = self.get_resp(self.sig(self.OP_GET))
            return self._label.replace('%l', text)

        active_widgets = self._widgets
        label_parts = re.split('(<span.*?>.*?</span>)', self._label)
        widget_index = 0
        for part in label_parts:
            part = part.strip()
            if part and widget_index < len(active_widgets) and isinstance(active_widgets[widget_index], QLabel):
                if '<span' in part and '</span>' in part:
                    icon = re.sub(r'<span.*?>|</span>', '', part).strip()
                    active_widgets[widget_index].setText(icon)
                else:
                    active_widgets[widget_index].setText(get_text())
                active_widgets[widget_index].show()
                widget_index += 1

    @staticmethod
    def get_resp(resp):
        if resp == OpenKeyWidget.EN:
            return str(os.environ['OKC_EN']) if 'OKC_EN' in os.environ else 'EN'
        elif resp == OpenKeyWidget.VN:
            return str(os.environ['OKC_VN']) if 'OKC_VN' in os.environ else 'VN'
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

    def toggle_im(self):
        self.sig(self.OP_TOGGLE)

    def toggle_control_panel(self):
        self.sig(self.OP_CONTROL_PANEL)