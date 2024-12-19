# commands/camera_controls/controller.py
import inquirer
from rich.console import Console
from obsbot_cli.commands.camera import CameraCommands
from .interactive_mode import InteractiveModeController
from .precise_mode import PreciseModeController
from .utils.conversion import AngleConverter

console = Console()

class CameraControlCommands:
   """🎮 Camera manual control handler"""

   def __init__(self, device):
       self.device = device
       self.camera = CameraCommands(device)
       self.interactive_mode = InteractiveModeController(self.camera)
       self.precise_mode = PreciseModeController(self.camera)
       self.angle_converter = AngleConverter()

   def handle(self):
       """🎮 Handle camera controls menu interaction"""
       while True:
           current_pos = self.camera.controller.get_current_position()
           pan_deg = self.angle_converter.to_degrees(current_pos['pan'], 'pan')
           tilt_deg = self.angle_converter.to_degrees(current_pos['tilt'], 'tilt')

           console.print(f"\n[blue]📍 Current Position:[/blue]")
           console.print(f"👈 Pan: {pan_deg}° | 👆 Tilt: {tilt_deg}° | 🔍 Zoom: {current_pos['zoom']}%")

           questions = [
               inquirer.List('control',
                   message="Select control mode",
                   choices=[
                       '🕹️  Interactive Control (Arrow Keys)',
                       '📏 Precise Control (Step Values)',
                       '🎯 Center Camera',
                       '↩️  Back to Main Menu'
                   ]
               )
           ]

           result = inquirer.prompt(questions)
           if not result or result['control'] == '↩️  Back to Main Menu':
               break

           if result['control'] == '🎯 Center Camera':
               self.camera.center()
           elif result['control'] == '🕹️  Interactive Control (Arrow Keys)':
               self.interactive_mode.start()
           elif result['control'] == '📏 Precise Control (Step Values)':
               self.precise_mode.start()