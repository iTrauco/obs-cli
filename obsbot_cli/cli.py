# obsbot_cli/cli.py
import click
from rich.console import Console
import inquirer
import sys

console = Console()

def print_header():
    console.print("\n[bold blue]=== OBSBOT Camera Controller ===[/bold blue]\n")

@click.command()
@click.option('--device', default='/dev/video9', help='Camera device path')
def main(device):
    """Interactive OBSBOT Camera Control"""
    print_header()
    
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
            
            # Handle Ctrl+C or cancellation
            if result is None:
                console.print("\n[yellow]Goodbye![/yellow]")
                sys.exit(0)
                
            action = result['action']
            
            if action == 'Exit':
                console.print("[yellow]Goodbye![/yellow]")
                break
                
            console.print(f"Selected: {action}")

    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
        sys.exit(0)

if __name__ == '__main__':
    main()