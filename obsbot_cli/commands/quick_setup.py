
import inquirer
from rich.console import Console
from obsbot_cli.commands.camera import CameraCommands

console = Console()

class QuickSetupCommands:
    """Quick setup mode command handler"""
    
    def __init__(self, device):
        self.device = device
        self.camera = CameraCommands(device)
    
    def handle(self):
        """Handle quick setup menu interaction"""
        questions = [
            inquirer.List('mode',
                message="Select quick setup mode",
                choices=[
                    'Presentation',
                    'Meeting',
                    'Wide Room',
                    'Back'
                ]
            )
        ]
        
        result = inquirer.prompt(questions)
        if not result or result['mode'] == 'Back':
            return

        mode = result['mode'].lower()
        if mode == 'presentation':
            self.camera.presentation_mode()
        elif mode == 'meeting':
            self.camera.meeting_mode()
        elif mode == 'wide room':
            self.camera.wide_room_mode()