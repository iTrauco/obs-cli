import subprocess
from rich.console import Console
from obsbot_cli.config.settings import CAMERA_SETTINGS

console = Console()

class CameraController:
    """Camera control implementation."""
    
    def __init__(self, device):
        self.device = device
    
    def set_control(self, control, value):
        """Set a v4l2 control value."""
        try:
            cmd = ['sudo', 'v4l2-ctl', '-d', self.device, f'--set-ctrl={control}={value}']
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            console.print(f"[red]Error setting {control} to {value}[/red]")
            return False
    
    def center_camera(self):
        """Center all camera positions."""
        self.set_control('pan_absolute', 0)
        self.set_control('tilt_absolute', 0)
        self.set_control('zoom_absolute', 0)
        console.print("[green]Camera centered[/green]")
    
    def presentation_mode(self):
        """Set up camera for presentation."""
        self.set_control('zoom_absolute', 50)
        self.set_control('pan_absolute', 0)
        self.set_control('tilt_absolute', 0)
        console.print("[green]Presentation mode activated[/green]")
    
    def start_preview(self):
        """Start camera preview."""
        try:
            subprocess.Popen(['vlc', f'v4l2://{self.device}'])
            console.print("[green]Preview started[/green]")
        except Exception as e:
            console.print(f"[red]Error starting preview: {e}[/red]")
    
    def test_movement(self):
        """Run movement test pattern."""
        console.print("[yellow]Running movement test...[/yellow]")
        # Pan test
        self.set_control('pan_absolute', -100000)
        self.set_control('pan_absolute', 100000)
        self.set_control('pan_absolute', 0)
        # Tilt test
        self.set_control('tilt_absolute', -100000)
        self.set_control('tilt_absolute', 100000)
        self.set_control('tilt_absolute', 0)
        # Zoom test
        self.set_control('zoom_absolute', 100)
        self.set_control('zoom_absolute', 0)
        console.print("[green]Movement test complete[/green]")