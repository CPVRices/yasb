"""
This is very experimental and may not work as expected. It uses ctypes to interact with the Windows Bluetooth API. We need to test this on more systems to ensure it works as expected.
"""
import re
import ctypes
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from ctypes import wintypes
from core.widgets.base import BaseWidget
from core.validation.widgets.yasb.bluetooth import VALIDATION_SCHEMA
import os
from settings import DEBUG
import logging

def get_bluetooth_api():
    """Get Bluetooth API with fallbacks since the DLL may not be in the same location on all systems."""
    possible_paths = [
        "BluetoothAPIs.dll",
        os.path.join(os.environ['SystemRoot'], 'System32', 'BluetoothAPIs.dll'),
        os.path.join(os.environ['SystemRoot'], 'SysWOW64', 'BluetoothAPIs.dll') # For 32-bit Python on 64-bit Windows
    ]
    
    for path in possible_paths:
        try:
            return ctypes.WinDLL(path)
        except (WindowsError, OSError) as e:
            last_error = e
            continue
            
    raise RuntimeError(f"Failed to load BluetoothAPIs.dll. Error: {last_error}")

# Define SYSTEMTIME structure
class SYSTEMTIME(ctypes.Structure):
    _fields_ = [
        ('wYear', wintypes.WORD),
        ('wMonth', wintypes.WORD),
        ('wDayOfWeek', wintypes.WORD),
        ('wDay', wintypes.WORD),
        ('wHour', wintypes.WORD),
        ('wMinute', wintypes.WORD),
        ('wSecond', wintypes.WORD),
        ('wMilliseconds', wintypes.WORD),
    ]

# Define BLUETOOTH_DEVICE_INFO structure
class BLUETOOTH_DEVICE_INFO(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("Address", ctypes.c_ulonglong),
        ("ulClassofDevice", wintypes.ULONG),
        ("fConnected", wintypes.BOOL),
        ("fRemembered", wintypes.BOOL),
        ("fAuthenticated", wintypes.BOOL),
        ("stLastSeen", SYSTEMTIME),
        ("stLastUsed", SYSTEMTIME),
        ("szName", ctypes.c_wchar * 248),
    ]

# Define BLUETOOTH_DEVICE_SEARCH_PARAMS structure
class BLUETOOTH_DEVICE_SEARCH_PARAMS(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("fReturnAuthenticated", wintypes.BOOL),
        ("fReturnRemembered", wintypes.BOOL),
        ("fReturnUnknown", wintypes.BOOL),
        ("fReturnConnected", wintypes.BOOL),
        ("fIssueInquiry", wintypes.BOOL),
        ("cTimeoutMultiplier", ctypes.c_ubyte),
        ("hRadio", wintypes.HANDLE),
    ]

# Define BLUETOOTH_FIND_RADIO_PARAMS structure
class BLUETOOTH_FIND_RADIO_PARAMS(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
    ]

class BluetoothThread(QThread):
    status_signal = pyqtSignal(str)

    def __init__(self, bt_api):
        super().__init__()
        self.bt_api = bt_api

    def run(self):
        status = self.get_bluetooth_status()
        self.status_signal.emit(status)

    def is_bluetooth_enabled(self):
        find_radio_params = BLUETOOTH_FIND_RADIO_PARAMS(
            dwSize=ctypes.sizeof(BLUETOOTH_FIND_RADIO_PARAMS)
        )
        radio_handle = wintypes.HANDLE()
        find_first_radio = self.bt_api.BluetoothFindFirstRadio
        find_first_radio.argtypes = [
            ctypes.POINTER(BLUETOOTH_FIND_RADIO_PARAMS),
            ctypes.POINTER(wintypes.HANDLE),
        ]
        find_first_radio.restype = wintypes.HANDLE  # Correct restype for a handle
        radio_finder = find_first_radio(
            ctypes.byref(find_radio_params), ctypes.byref(radio_handle)
        )
        if radio_finder and radio_finder != wintypes.HANDLE(0):
            # Define argtypes and restype for BluetoothFindRadioClose
            self.bt_api.BluetoothFindRadioClose.argtypes = [wintypes.HANDLE]
            self.bt_api.BluetoothFindRadioClose.restype = wintypes.BOOL
            self.bt_api.BluetoothFindRadioClose.argtypes = [wintypes.HANDLE]
            self.bt_api.BluetoothFindRadioClose.restype = wintypes.BOOL
            self.bt_api.BluetoothFindRadioClose(radio_finder)
            ctypes.windll.kernel32.CloseHandle(radio_handle)
            return True
        return False

    def get_bluetooth_devices(self):
        devices = []
        find_radio_params = BLUETOOTH_FIND_RADIO_PARAMS(
            dwSize=ctypes.sizeof(BLUETOOTH_FIND_RADIO_PARAMS)
        )
        radio_handle = wintypes.HANDLE()
        find_first_radio = self.bt_api.BluetoothFindFirstRadio
        find_first_radio.argtypes = [
            ctypes.POINTER(BLUETOOTH_FIND_RADIO_PARAMS),
            ctypes.POINTER(wintypes.HANDLE),
        ]
        find_first_radio.restype = wintypes.HANDLE
        radio_finder = find_first_radio(
            ctypes.byref(find_radio_params), ctypes.byref(radio_handle)
        )
        if not radio_finder or radio_finder == wintypes.HANDLE(0):
            return devices
        try:
            while True:
                device_search_params = BLUETOOTH_DEVICE_SEARCH_PARAMS(
                    dwSize=ctypes.sizeof(BLUETOOTH_DEVICE_SEARCH_PARAMS),
                    fReturnAuthenticated=True,
                    fReturnRemembered=True,
                    fReturnUnknown=False,
                    fReturnConnected=True,
                    fIssueInquiry=False,
                    cTimeoutMultiplier=1,
                    hRadio=radio_handle,
                )
                device_info = BLUETOOTH_DEVICE_INFO()
                device_info.dwSize = ctypes.sizeof(BLUETOOTH_DEVICE_INFO)
                find_first_device = self.bt_api.BluetoothFindFirstDevice
                find_first_device.argtypes = [
                    ctypes.POINTER(BLUETOOTH_DEVICE_SEARCH_PARAMS),
                    ctypes.POINTER(BLUETOOTH_DEVICE_INFO),
                ]
                find_first_device.restype = wintypes.HANDLE
                device_finder = find_first_device(
                    ctypes.byref(device_search_params), ctypes.byref(device_info)
                )
                if not device_finder or device_finder == wintypes.HANDLE(0):
                    break
                try:
                    while True:
                        address = ':'.join(
                            [
                                '%02X' % ((device_info.Address >> (8 * i)) & 0xFF)
                                for i in range(6)
                            ][::-1]
                        )
                        devices.append(
                            {
                                "name": device_info.szName,
                                "address": address,
                                "connected": bool(device_info.fConnected),
                                "authenticated": bool(device_info.fAuthenticated)
                            }
                        )
                        next_device = self.bt_api.BluetoothFindNextDevice
                        next_device.argtypes = [
                            wintypes.HANDLE,
                            ctypes.POINTER(BLUETOOTH_DEVICE_INFO),
                        ]
                        next_device.restype = wintypes.BOOL
                        if not next_device(device_finder, ctypes.byref(device_info)):
                            break
                finally:
                    self.bt_api.BluetoothFindDeviceClose.argtypes = [wintypes.HANDLE]
                    self.bt_api.BluetoothFindDeviceClose.restype = wintypes.BOOL
                    self.bt_api.BluetoothFindDeviceClose(device_finder)
                # Move to the next radio (if any)
                next_radio = self.bt_api.BluetoothFindNextRadio
                next_radio.argtypes = [
                    wintypes.HANDLE,
                    ctypes.POINTER(wintypes.HANDLE),
                ]
                next_radio.restype = wintypes.BOOL
                if not next_radio(radio_finder, ctypes.byref(radio_handle)):
                    break
        finally:
            self.bt_api.BluetoothFindRadioClose(radio_finder)
            ctypes.windll.kernel32.CloseHandle(radio_handle)
        return devices

    def get_bluetooth_status(self):
        if self.is_bluetooth_enabled():
            devices = self.get_bluetooth_devices()
            if devices:
                # Only show devices that are both connected AND authenticated (paired)
                connected_devices = [
                    device['name'] 
                    for device in devices 
                    if device['connected'] and device['authenticated']  # Add authenticated check
                ]
                if connected_devices:
                    return f"Connected to: {', '.join(connected_devices)}"
            return "Bluetooth is on, but no paired devices connected."
        return "Bluetooth is disabled."

class BluetoothWidget(BaseWidget):
    validation_schema = VALIDATION_SCHEMA

    def __init__(
        self,
        label: str,
        label_alt: str,
        icons: dict[str, str],
        container_padding: dict[str, int],
        callbacks: dict[str, str]
    ):
        super().__init__(class_name="bluetooth-widget")
        self._show_alt_label = False
        self._label_content = label
        self._label_alt_content = label_alt
        self._padding = container_padding
        try:
            self.bt_api = get_bluetooth_api()
        except RuntimeError as e:
            if DEBUG:
                logging.error(f"Bluetooth support unavailable: {e}")
            self.bt_api = None
        self.current_status = None
        self._icons = icons
        
        self.bluetooth_icon = None
        self.connected_devices = None
        
        self._widget_container_layout: QHBoxLayout = QHBoxLayout()
        self._widget_container_layout.setSpacing(0)
        self._widget_container_layout.setContentsMargins(self._padding['left'], self._padding['top'], self._padding['right'], self._padding['bottom'])
        self._widget_container: QWidget = QWidget()
        self._widget_container.setLayout(self._widget_container_layout)
        self._widget_container.setProperty("class", "widget-container")
        self.widget_layout.addWidget(self._widget_container)
        self._create_dynamically_label(self._label_content, self._label_alt_content)

        self.register_callback("toggle_label", self._toggle_label)
 
        self.callback_left = callbacks['on_left']
        self.callback_right = callbacks['on_right']
        self.callback_middle = callbacks['on_middle']
   
 

        self.current_status = None  # Store the current Bluetooth status
        self.bluetooth_thread = BluetoothThread(self.bt_api)
        self.bluetooth_thread.status_signal.connect(self._update_state)

         # Setup QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_bluetooth_thread)
        self.timer.start(3000)

        self.start_bluetooth_thread()
        self._update_label(self._icons['bluetooth_off'])
        
        
    def start_bluetooth_thread(self):
        if not self.bluetooth_thread.isRunning():
            self.bluetooth_thread = BluetoothThread(self.bt_api)
            self.bluetooth_thread.status_signal.connect(self._update_state)
            self.bluetooth_thread.start()
            
    def stop(self):
        self.timer.stop()
        if self.bluetooth_thread.isRunning():
            self.bluetooth_thread.terminate()
            self.bluetooth_thread.wait()
            
    def _toggle_label(self):
        self._show_alt_label = not self._show_alt_label
        for widget in self._widgets:
            widget.setVisible(not self._show_alt_label)
        for widget in self._widgets_alt:
            widget.setVisible(self._show_alt_label)
        self._update_label(self.bluetooth_icon,self.connected_devices)

    def _create_dynamically_label(self, content: str, content_alt: str):
        def process_content(content, is_alt=False):
            label_parts = re.split('(<span.*?>.*?</span>)', content)
            label_parts = [part for part in label_parts if part]
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
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self._widget_container_layout.addWidget(label)
                widgets.append(label)
                if is_alt:
                    label.hide()
                else:
                    label.show()
            return widgets
        self._widgets = process_content(content)
        self._widgets_alt = process_content(content_alt, is_alt=True)


    def _update_label(self, icon, connected_devices=None):
        active_widgets = self._widgets_alt if self._show_alt_label else self._widgets
        active_label_content = self._label_alt_content if self._show_alt_label else self._label_content
        label_parts = re.split('(<span.*?>.*?</span>)', active_label_content)
        label_parts = [part for part in label_parts if part]
        widget_index = 0

        if connected_devices:
            device_names = ", ".join(connected_devices)
            tooltip_text = "Connected devices\n" + "\n".join(f"• {name}" for name in connected_devices) if connected_devices else "No devices connected"
        else:
            device_names = "No devices connected"
            tooltip_text = "No devices connected"

        label_options = {
            "{icon}": icon,
            "{device_name}": device_names
        }

        for part in label_parts:
            part = part.strip()
            if part:
                formatted_text = part
                for option, value in label_options.items():
                    formatted_text = formatted_text.replace(option, str(value))
                if '<span' in part and '</span>' in part:
                    if widget_index < len(active_widgets) and isinstance(active_widgets[widget_index], QLabel):
                        active_widgets[widget_index].setText(formatted_text)
                else:
                    if widget_index < len(active_widgets) and isinstance(active_widgets[widget_index], QLabel):
                        active_widgets[widget_index].setText(formatted_text)
                widget_index += 1

        # Set tooltip with connected device names
        self._widget_container.setToolTip(tooltip_text)

    def _update_state(self, status):
        self.current_status = status
        if DEBUG and self.current_status != "Bluetooth is disabled.":
            logging.info(f"Bluetooth: {self.current_status}")

        if not self.current_status:  # Handle None case
            return self._icons['bluetooth_off']

        if self.current_status == "Bluetooth is disabled.":
            bluetooth_icon = self._icons['bluetooth_off']
            connected_devices = None
        elif "Connected to" in self.current_status:
            bluetooth_icon = self._icons['bluetooth_connected']
            connected_devices = self.current_status.replace("Connected to: ", "").split(", ")
        else:
            bluetooth_icon = self._icons['bluetooth_on']
            connected_devices = None
        self.bluetooth_icon = bluetooth_icon
        self.connected_devices = connected_devices
        self._update_label(bluetooth_icon, connected_devices)