# obsbot_cli/config/settings.py
"""⚙️ Configuration settings for the OBSBOT camera."""

# 📐 Camera movement limits and defaults
CAMERA_SETTINGS = {
    'pan': {
        'min': -468000,
        'max': 468000,
        'default': 0
    },
    'tilt': {
        'min': -324000,
        'max': 324000,
        'default': 0
    },
    'zoom': {
        'min': 0,
        'max': 100,
        'default': 0
    }
}

# 🎯 Quick setup mode presets
QUICK_SETUP_MODES = {
    'presentation': {
        'zoom': 50,
        'pan': 0,
        'tilt': 0
    },
    'meeting': {
        'zoom': 30,
        'pan': 0,
        'tilt': 0
    },
    'wide_room': {
        'zoom': 0,
        'pan': 0,
        'tilt': 0
    }
}