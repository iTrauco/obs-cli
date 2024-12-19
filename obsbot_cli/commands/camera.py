from rich.console import Console
from obsbot_cli.utils.v4l2 import V4L2Controller
from obsbot_cli.config.settings import CAMERA_SETTINGS, QUICK_SETUP_MODES

console = Console()

class CameraCommands:
    """🎥 Core camera control commands"""
    
    def __init__(self, device):
        """🔌 Initialize camera controller"""
        self.device = device
        self.controller = V4L2Controller(device)
    
    def center(self):
        """⭕ Center all camera positions"""
        console.print("[yellow]Centering camera...[/yellow]")
        success = True
        success &= self.controller.set_pan(CAMERA_SETTINGS['pan']['default'])
        success &= self.controller.set_tilt(CAMERA_SETTINGS['tilt']['default'])
        success &= self.controller.set_zoom(CAMERA_SETTINGS['zoom']['default'])
        if success:
            console.print("[green]Camera centered successfully[/green]")
        return success

    def presentation_mode(self):
        """🎯 Set up camera for presentation"""
        console.print("[yellow]Setting up presentation mode...[/yellow]")
        mode = QUICK_SETUP_MODES['presentation']
        success = True
        success &= self.controller.set_zoom(mode['zoom'])
        success &= self.controller.set_pan(mode['pan'])
        success &= self.controller.set_tilt(mode['tilt'])
        if success:
            console.print("[green]Presentation mode activated[/green]")
        return success
    
    def meeting_mode(self):
        """👥 Set up camera for meeting"""
        console.print("[yellow]Setting up meeting mode...[/yellow]")
        mode = QUICK_SETUP_MODES['meeting']
        success = True
        success &= self.controller.set_zoom(mode['zoom'])
        success &= self.controller.set_pan(mode['pan'])
        success &= self.controller.set_tilt(mode['tilt'])
        if success:
            console.print("[green]Meeting mode activated[/green]")
        return success
    
    def wide_room_mode(self):
        """🏠 Set up camera for wide room view"""
        console.print("[yellow]Setting up wide room mode...[/yellow]")
        mode = QUICK_SETUP_MODES['wide_room']
        success = True
        success &= self.controller.set_zoom(mode['zoom'])
        success &= self.controller.set_pan(mode['pan'])
        success &= self.controller.set_tilt(mode['tilt'])
        if success:
            console.print("[green]Wide room mode activated[/green]")
        return success

    def test_movement(self):
        """🔄 Run camera movement test pattern"""
        console.print("[yellow]Starting movement test...[/yellow]")
        success = True
        
        # Test pan
        console.print("[blue]Debug: Starting pan test...[/blue]")
        console.print("Testing pan movement...")
        success &= self.controller.set_pan(-100000)
        console.print(f"[blue]Debug: Pan -100000 completed. Success={success}[/blue]")
        success &= self.controller.set_pan(100000)
        console.print(f"[blue]Debug: Pan 100000 completed. Success={success}[/blue]")
        success &= self.controller.set_pan(0)
        console.print(f"[blue]Debug: Pan center completed. Success={success}[/blue]")
        
        # Test tilt
        console.print("[blue]Debug: Starting tilt test...[/blue]")
        console.print("Testing tilt movement...")
        success &= self.controller.set_tilt(-100000)
        console.print(f"[blue]Debug: Tilt -100000 completed. Success={success}[/blue]")
        success &= self.controller.set_tilt(100000)
        console.print(f"[blue]Debug: Tilt 100000 completed. Success={success}[/blue]")
        success &= self.controller.set_tilt(0)
        console.print(f"[blue]Debug: Tilt center completed. Success={success}[/blue]")
        
        # Test zoom
        console.print("[blue]Debug: Starting zoom test...[/blue]")
        console.print("Testing zoom movement...")
        success &= self.controller.set_zoom(100)
        console.print(f"[blue]Debug: Zoom 100 completed. Success={success}[/blue]")
        success &= self.controller.set_zoom(0)
        console.print(f"[blue]Debug: Zoom 0 completed. Success={success}[/blue]")
        
        if success:
            console.print("[green]Movement test completed successfully[/green]")
        else:
            console.print("[red]Movement test completed with errors[/red]")
        return success
