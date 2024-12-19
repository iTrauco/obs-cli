# obsbot_cli/utils/menu.py
import inquirer
from rich.console import Console

console = Console()

class MenuManager:
    def main_menu(self):
        """Show main menu"""
        questions = [
            inquirer.List('action',
                message="Select an action",
                choices=[
                    'Quick Setup',
                    'Camera Controls',
                    'Preview',
                    'Presets',
                    'Test Movement',
                    'Exit'
                ]
            )
        ]
        return inquirer.prompt(questions)['action']
    
    def quick_setup_menu(self):
        """Show quick setup menu"""
        questions = [
            inquirer.List('setup',
                message="Select quick setup mode",
                choices=[
                    'Presentation',
                    'Meeting',
                    'Wide Room',
                    'Back'
                ]
            )
        ]
        return inquirer.prompt(questions)['setup']
    
    def camera_control_menu(self):
        """Show camera control menu"""
        questions = [
            inquirer.List('control',
                message="Select control to adjust",
                choices=[
                    'Pan',
                    'Tilt',
                    'Zoom',
                    'Center',
                    'Back'
                ]
            )
        ]
        return inquirer.prompt(questions)['control']
    
    def preset_menu(self):
        """Show preset menu"""
        questions = [
            inquirer.List('preset',
                message="Select preset action",
                choices=[
                    'Save Current',
                    'Load',
                    'Back'
                ]
            )
        ]
        return inquirer.prompt(questions)['preset']
    
    def get_number_input(self, message, min_val, max_val):
        """Get validated number input"""
        while True:
            questions = [
                inquirer.Text('value', message=message)
            ]
            try:
                value = int(inquirer.prompt(questions)['value'])
                if min_val <= value <= max_val:
                    return value
                console.print(f"[red]Value must be between {min_val} and {max_val}[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number[/red]")
    
    def get_text_input(self, message):
        """Get text input"""
        questions = [
            inquirer.Text('value', message=message)
        ]
        return inquirer.prompt(questions)['value']
    
    def select_preset(self, presets):
        """Select from available presets"""
        questions = [
            inquirer.List('preset',
                message="Select preset",
                choices=presets + ['Back']
            )
        ]
        return inquirer.prompt(questions)['preset']
