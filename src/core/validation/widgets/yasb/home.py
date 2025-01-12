DEFAULTS = {
    'label': '\ue71a',
    'container_padding': {'top': 0, 'left': 0, 'bottom': 0, 'right': 0},
    'power_menu': True,
    'system_menu': True,
    'blur': False,
    'round_corners': True,
    'round_corners_type': 'normal',
    'border_color': 'System',
    'alignment': 'left',
    'direction': 'down',
    'distance': 6,
    'menu_labels': {'shutdown': 'Shutdown', 'restart': 'Restart', 'logout': 'Logout', 'lock': 'Lock', 'sleep': 'Sleep', 'system': 'System Settings', 'about': 'About This PC', 'task_manager': 'Task Manager'},
    'animation': {
        'enabled': True,
        'type': 'fadeInOut',
        'duration': 200
    },
    'callbacks': {
        'on_left': 'toggle_menu'
    }
}

VALIDATION_SCHEMA = {
    'label': {
        'type': 'string',
        'default': DEFAULTS['label']
    },
    'menu_list': {
        'required': False,
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'title': {'type': 'string'},
                'path': {'type': 'string'}
            }
        }
    },
    'container_padding': {
        'type': 'dict',
        'default': DEFAULTS['container_padding'],
        'required': False
    },
    'power_menu': {
        'type': 'boolean',
        'default': DEFAULTS['power_menu'],
        'required': False
    },
    'system_menu': {
        'type': 'boolean',
        'default': DEFAULTS['system_menu'],
        'required': False
    },
    'blur': {
        'type': 'boolean',
        'default': DEFAULTS['blur'],
        'required': False
    },
    'round_corners': {
        'type': 'boolean',
        'default': DEFAULTS['round_corners'],
        'required': False
    },
    'round_corners_type': {
        'type': 'string',
        'default': DEFAULTS['round_corners_type'],
        'required': False
    },
    'border_color': {
        'type': 'string',
        'default': DEFAULTS['border_color'],
        'required': False
    },
    'alignment': {
        'type': 'string',
        'default': DEFAULTS['alignment'],
        'required': False
    },
    'direction': {
        'type': 'string',
        'default': DEFAULTS['direction'],
        'required': False
    },
    'distance': {
        'type': 'integer',
        'default': DEFAULTS['distance'],
        'required': False
    },
    'menu_labels': {
        'type': 'dict',
        'required': False,
        'schema': {
            'shutdown': {'type': 'string', 'default': DEFAULTS['menu_labels']['shutdown']},
            'restart': {'type': 'string', 'default': DEFAULTS['menu_labels']['restart']},
            'logout': {'type': 'string', 'default': DEFAULTS['menu_labels']['logout']},
            'lock': {'type': 'string', 'default': DEFAULTS['menu_labels']['lock']},
            'sleep': {'type': 'string', 'default': DEFAULTS['menu_labels']['sleep']},
            'system': {'type': 'string', 'default': DEFAULTS['menu_labels']['system']},
            'about': {'type': 'string', 'default': DEFAULTS['menu_labels']['about']},
            'task_manager': {'type': 'string', 'default': DEFAULTS['menu_labels']['task_manager']}
        },
        'default': DEFAULTS['menu_labels']
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
        'required': False,
        'type': 'dict',
        'schema': {
            'on_left': {
                'type': 'string',
                'default': DEFAULTS['callbacks']['on_left']
            }
        },
        'default': DEFAULTS['callbacks']
    }
}
