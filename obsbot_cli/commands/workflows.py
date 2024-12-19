# obsbot_cli/commands/workflows.py
import inquirer
from obsbot_cli.utils.camera import CameraController
from obsbot_cli.utils.menu import MenuManager
from rich.console import Console

console = Console()

class WorkflowManager:
    def __init__(self, device):
        self.camera = CameraController(device)
        self.menu = MenuManager()
        
    def start(self):
        """Start the main workflow loop"""
        while True:
            action = self.menu.main_menu()
            
            if action == 'Exit':
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            if action == 'Quick Setup':
                self._handle_quick_setup()
            elif action == 'Camera Controls':
                self._handle_camera_controls()
            elif action == 'Preview':
                self._handle_preview()
            elif action == 'Presets':
                self._handle_presets()
            elif action == 'Test Movement':
                self._handle_test()
    
    def _handle_quick_setup(self):
        """Handle quick setup workflow"""
        setup = self.menu.quick_setup_menu()
        if setup == 'Presentation':
            self.camera.presentation_mode()
        elif setup == 'Meeting':
            self.camera.meeting_mode()
        elif setup == 'Wide Room':
            self.camera.wide_room_mode()
        
        self._wait_for_continue()
    
    def _handle_camera_controls(self):
        """Handle camera control workflow"""
        while True:
            control = self.menu.camera_control_menu()
            if control == 'Back':
                break
                
            if control == 'Pan':
                value = self.menu.get_number_input("Enter pan value (-468000 to 468000): ", -468000, 468000)
                self.camera.set_pan(value)
            elif control == 'Tilt':
                value = self.menu.get_number_input("Enter tilt value (-324000 to 324000): ", -324000, 324000)
                self.camera.set_tilt(value)
            elif control == 'Zoom':
                value = self.menu.get_number_input("Enter zoom value (0-100): ", 0, 100)
                self.camera.set_zoom(value)
            elif control == 'Center':
                self.camera.center()
                
            self._wait_for_continue()
    
    def _handle_preview(self):
        """Handle preview workflow"""
        self.camera.start_preview()
        self._wait_for_continue()
    
    def _handle_presets(self):
        """Handle presets workflow"""
        while True:
            preset = self.menu.preset_menu()
            if preset == 'Back':
                break
                
            if preset == 'Save Current':
                name = self.menu.get_text_input("Enter preset name: ")
                self.camera.save_preset(name)
            elif preset == 'Load':
                presets = self.camera.list_presets()
                if presets:
                    selected = self.menu.select_preset(presets)
                    self.camera.load_preset(selected)
                else:
                    console.print("[red]No presets saved yet[/red]")
            
            self._wait_for_continue()
    
    def _handle_test(self):
        """Handle test movement workflow"""
        self.camera.test_movement()
        self._wait_for_continue()
    
    def _wait_for_continue(self):
        """Wait for user to continue"""
        questions = [inquirer.Confirm('continue', message='Press Enter to continue')]
        inquirer.prompt(questions)