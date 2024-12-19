# obsbot_cli/cli.py
import click
from rich.console import Console
import inquirer
import sys
from obsbot_cli.commands.quick_setup import QuickSetupCommands
from obsbot_cli.commands.camera import CameraCommands  # Add this importfrom obsbot_cli.commands.preview import PreviewCommands
from obsbot_cli.commands.preview import PreviewCommands



console = Console()

def print_header():
    console.print("\n[bold blue]=== OBSBOT Camera Controller ===[/bold blue]\n")

@click.command()
@click.option('--device', default='/dev/video9', help='Camera device path')
def main(device):
    """Interactive OBSBOT Camera Control"""
    print_header()
    
    # Initialize command handlers
    quick_setup = QuickSetupCommands(device)
    camera = CameraCommands(device)  # Add this linepreview = PreviewCommands(device)
    preview = PreviewCommands(device)


    
    try:
        while True:
            questions = [
                inquirer.List('action',
                    message="Select an action",
                    choices=[
                        'Quick Setup',
                        'Camera Controls',
                        'Preview',
                        'Test Movement',
                        'Exit'
                    ]
                )
            ]
            
            result = inquirer.prompt(questions)
            
            if result is None:
                console.print("\n[yellow]Goodbye![/yellow]")
                sys.exit(0)
                
            action = result['action']
            
            if action == 'Exit':
                console.print("[yellow]Goodbye![/yellow]")
                break
            elif action == 'Quick Setup':
                quick_setup.handle()
            elif action == 'Test Movement':  # Add this block
                camera.test_movement()
            elif action == 'Preview':
                preview.handle()


    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
        sys.exit(0)

if __name__ == '__main__':
    main()