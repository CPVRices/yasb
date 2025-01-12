DEFAULTS = {
    'label_max_length': None,
    'exec_options': {
        'run_cmd': None,
        'run_once': False,
        'run_interval': 0,
        'return_format': "json",
        'hide_empty': False
    },
    'animation': {
        'enabled': True,
        'type': 'fadeInOut',
        'duration': 200
    },
    'callbacks': {
        'on_left': "toggle_label",
        'on_middle': "do_nothing",
        'on_right': "do_nothing",
    }
}


VALIDATION_SCHEMA = {
    'class_name': {
        'type': 'string',
        'required': True,
    },
    'label': {
        'type': 'string',
        'required': True
    },
    'label_alt': {
        'type': 'string',
        'default': True
    },
    'label_max_length': {
        'type': 'integer',
        'nullable': True,
        'default': DEFAULTS['label_max_length'],
        'min': 1
    },
    'exec_options': {
        'type': 'dict',
        'schema': {
            'run_cmd': {
                'type': 'string',
                'nullable': True,
                'default': DEFAULTS['exec_options']['run_cmd']
            },
            'run_once': {
                'type': 'boolean',
                'default': DEFAULTS['exec_options']['run_once']
            },
            'run_interval': {
                'type': 'integer',
                'default': DEFAULTS['exec_options']['run_interval'],
                'min': 0
            },
            'return_format': {
                'type': 'string',
                'allowed': ['string', 'json'],
                'default': DEFAULTS['exec_options']['return_format']
            },
            'hide_empty': {
                'type': 'boolean',
                'required': False,
                'default': DEFAULTS['exec_options']['hide_empty']
            }
        },
        'default': DEFAULTS['exec_options']
    },
    'animation': {
        'type': 'dict',
        'required': False,
        'schema': {
            'enabled': {
                'type': 'boolean',
                'default': DEFAULTS['animation']['enabled']
            },
            'type': {
                'type': 'string',
                'default': DEFAULTS['animation']['type']
            },
            'duration': {
                'type': 'integer',
                'default': DEFAULTS['animation']['duration']
            }
        },
        'default': DEFAULTS['animation']
    },
    'callbacks': {
        'type': 'dict',
        'schema': {
            'on_left': {
                'type': 'string',
                'default': DEFAULTS['callbacks']['on_left'],
            },
            'on_middle': {
                'type': 'string',
                'default': DEFAULTS['callbacks']['on_middle'],
            },
            'on_right': {
                'type': 'string',
                'default': DEFAULTS['callbacks']['on_right']
            }
        },
        'default': DEFAULTS['callbacks']
    }
}
