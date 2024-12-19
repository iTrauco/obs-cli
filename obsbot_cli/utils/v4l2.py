# obsbot_cli/utils/v4l2.py
import subprocess
from rich.console import Console
from obsbot_cli.config.settings import CAMERA_SETTINGS

console = Console()

class V4L2Controller:
    """🎮 Low-level V4L2 control implementation"""
    
    def __init__(self, device):
        self.device = device
    
    def set_control(self, control, value):
        """🎮 Set a v4l2 control value"""
        try:
            cmd = ['v4l2-ctl', '-d', self.device, f'--set-ctrl={control}={value}']
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error setting {control} to {value}: {e.stderr.decode()}[/red]")
            return False
    
    def get_control(self, control):
        """📊 Get current value of a v4l2 control"""
        try:
            cmd = ['v4l2-ctl', '-d', self.device, f'--get-ctrl={control}']
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            value = int(result.stdout.split(':')[1].strip())
            return value
        except (subprocess.CalledProcessError, ValueError, IndexError) as e:
            console.print(f"[red]Error getting {control} value: {e}[/red]")
            return None

    def set_pan(self, value):
        """👈 Set camera pan position"""
        if CAMERA_SETTINGS['pan']['min'] <= value <= CAMERA_SETTINGS['pan']['max']:
            return self.set_control('pan_absolute', value)
        console.print(f"[red]Pan value must be between {CAMERA_SETTINGS['pan']['min']} and {CAMERA_SETTINGS['pan']['max']}[/red]")
        return False
    
    def set_tilt(self, value):
        """👆 Set camera tilt position"""
        if CAMERA_SETTINGS['tilt']['min'] <= value <= CAMERA_SETTINGS['tilt']['max']:
            return self.set_control('tilt_absolute', value)
        console.print(f"[red]Tilt value must be between {CAMERA_SETTINGS['tilt']['min']} and {CAMERA_SETTINGS['tilt']['max']}[/red]")
        return False
    
    def set_zoom(self, value):
        """🔍 Set camera zoom level"""
        if CAMERA_SETTINGS['zoom']['min'] <= value <= CAMERA_SETTINGS['zoom']['max']:
            return self.set_control('zoom_absolute', value)
        console.print(f"[red]Zoom value must be between {CAMERA_SETTINGS['zoom']['min']} and {CAMERA_SETTINGS['zoom']['max']}[/red]")
        return False

    def get_current_position(self):
        """📍 Get current camera position values"""
        return {
            'pan': self.get_control('pan_absolute'),
            'tilt': self.get_control('tilt_absolute'),
            'zoom': self.get_control('zoom_absolute')
        }