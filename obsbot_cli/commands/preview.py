# obsbot_cli/commands/preview.py
import subprocess
from rich.console import Console
import inquirer

console = Console()

class PreviewCommands:
    """🎬 Camera preview commands"""
    
    def __init__(self, device):
        self.device = device
        
    def start_preview(self):
        """Start camera preview using VLC"""
        try:
            subprocess.Popen(['vlc', f'v4l2://{self.device}'])
            console.print("[green]Preview started in VLC[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Error starting preview: {e}[/red]")
            return False
            
    def stop_preview(self):
        """Stop any running preview processes"""
        try:
            subprocess.run(['pkill', '-f', f'vlc.*{self.device}'])
            console.print("[green]Preview stopped[/green]")
            return True
        except Exception as e:
            console.print(f"[red]Error stopping preview: {e}[/red]")
            return False
        
    def handle(self):
        """🎬 Handle preview menu interaction"""
        while True:  # Add recursion
            questions = [
                inquirer.List('preview_action',
                    message="Select preview action",
                    choices=[
                        'Start Preview',
                        'Stop Preview',
                        'Back to Main Menu'
                    ]
                )
            ]
            
            result = inquirer.prompt(questions)
            if not result or result['preview_action'] == 'Back to Main Menu':
                break
                
            if result['preview_action'] == 'Start Preview':
                self.start_preview()
                console.print("[green]Preview running in background - you can continue using the menu[/green]")
            elif result['preview_action'] == 'Stop Preview':
                self.stop_preview()