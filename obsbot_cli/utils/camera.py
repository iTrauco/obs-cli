# obsbot_cli/utils/camera.py
import subprocess
import json
from pathlib import Path
from obsbot_cli.config.settings import PRESET_FILE

class CameraController:
    def __init__(self, device):
        self.device = device
        self._load_presets()
    
    def _load_presets(self):
        """Load saved presets"""
        self.presets = {}
        if Path(PRESET_FILE).exists():
            with open(PRESET_FILE, 'r') as f:
                self.presets = json.load(f)
    
    def _save_presets(self):
        """Save presets to file"""
        with open(PRESET_FILE, 'w') as f:
            json.dump(self.presets, f)
    
    def set_control(self, control, value):
        """Set a camera control"""
        cmd = ['sudo', 'v4l2-ctl', '-d', self.device, f'--set-ctrl={control}={value}']
        subprocess.run(cmd, check=True)
    
    def set_pan(self, value):
        self.set_control('pan_absolute', value)
    
    def set_tilt(self, value):
        self.set_control('tilt_absolute', value)
    
    def set_zoom(self, value):
        self.set_control('zoom_absolute', value)
    
    def center(self):
        """Center all camera controls"""
        self.set_pan(0)
        self.set_tilt(0)
        self.set_zoom(0)
    
    def start_preview(self):
        """Start camera preview"""
        subprocess.Popen(['vlc', f'v4l2://{self.device}'])
    
    def presentation_mode(self):
        """Set up for presentation"""
        self.set_zoom(50)
        self.center()
    
    def meeting_mode(self):
        """Set up for meeting"""
        self.set_zoom(30)
        self.center()
    
    def wide_room_mode(self):
        """Set up for wide room view"""
        self.set_zoom(0)
        self.center()
    
    def test_movement(self):
        """Run a movement test pattern"""
        # Pan left to right
        self.set_pan(-100000)
        self.set_pan(100000)
        self.set_pan(0)
        # Tilt up and down
        self.set_tilt(-100000)
        self.set_tilt(100000)
        self.set_tilt(0)
        # Zoom in and out
        self.set_zoom(100)
        self.set_zoom(0)