DEFAULTS = {
    'label': 'IM: %l',
    'update_interval': 50,
    'callbacks': {
        'on_left': 'toggle_im',
        'on_middle': 'do_nothing',
        'on_right': 'toggle_control_panel'
    }
}

VALIDATION_SCHEMA = {
    'label': {
        'type': 'string',
        'default': DEFAULTS['label']
    },
    'update_interval': {
        'type': 'integer',
        'default': 50,
        'min': 0,
        'max': 60000
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
                'default': DEFAULTS['callbacks']['on_right'],
            }
        },
        'default': DEFAULTS['callbacks']
    }
}
