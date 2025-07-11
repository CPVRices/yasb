from core.validation.bar import BAR_DEFAULTS, BAR_SCHEMA

CONFIG_SCHEMA = {
    "watch_config": {"type": "boolean", "default": True},
    "watch_stylesheet": {
        "type": "boolean",
        "default": True,
    },
    "debug": {
        "type": "boolean",
        "default": False,
        "required": False,
    },
    # env_file is deprecated and will be removed in the future
    # Use load .env file from the config folder instead
    "env_file": {
        "type": "string",
        "nullable": True,
        "required": False,
        "default": None,
    },
    "komorebi": {
        "type": "dict",
        "schema": {
            "start_command": {
                "type": "string",
                "required": False,
            },
            "stop_command": {
                "type": "string",
                "required": False,
            },
            "reload_command": {
                "type": "string",
                "required": False,
            },
        },
        "default": {
            "start_command": "komorebic start --whkd",
            "stop_command": "komorebic stop --whkd",
            "reload_command": "komorebic reload-configuration",
        },
    },
    "bars": {
        "type": "dict",
        "keysrules": {"type": "string"},
        "valuesrules": BAR_SCHEMA,
        "default": {"yasb-bar": BAR_DEFAULTS},
    },
    "widgets": {
        "type": "dict",
        "keysrules": {
            "type": "string",
        },
        "valuesrules": {"type": ["string", "dict"]},
        "default": {},
    },
}
