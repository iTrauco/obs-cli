# commands/camera_controls/precise_mode.py
import inquirer
from rich.console import Console
import time
from .utils.movement import MovementHandler
from .utils.conversion import AngleConverter

console = Console()

class PreciseModeController:
   """📏 Precise numeric camera control"""
   
   def __init__(self, camera):
       self.camera = camera
       self.movement_handler = MovementHandler(camera)
       self.angle_converter = AngleConverter()
       self.last_zoom_choice = 0  # Track last zoom selection

   def start(self):
       """Start precise control mode"""
       while True:
           current_pos = self.camera.controller.get_current_position()
           pan_deg = self.angle_converter.to_degrees(current_pos['pan'], 'pan')
           tilt_deg = self.angle_converter.to_degrees(current_pos['tilt'], 'tilt')

           console.print(f"\n[blue]Current Position:[/blue]")
           console.print(f"Pan: {pan_deg}° | Tilt: {tilt_deg}° | Zoom: {current_pos['zoom']}%")

           if not self._handle_control_selection(current_pos):
               break

   def _handle_control_selection(self, current_pos):
       """Handle main control type selection"""
       control_result = inquirer.prompt([
           inquirer.List('control',
               message="Select control to adjust",
               choices=[
                   '👈 Pan (Left/Right)',
                   '👆 Tilt (Up/Down)',
                   '🔍 Zoom (In/Out)',
                   '↩️ Back to Control Menu'
               ]
           )
       ])

       if not control_result or control_result['control'] == '↩️ Back to Control Menu':
           return False

       selected = control_result['control']
       if '👈 Pan' in selected:
           self._handle_movement_control('pan', True, current_pos)
       elif '👆 Tilt' in selected:
           self._handle_movement_control('tilt', False, current_pos)
       elif '🔍 Zoom' in selected:
           self._handle_zoom_control(current_pos)

       return True

   def _handle_movement_control(self, control_type, is_pan, current_pos):
       """Handle pan/tilt movement control"""
       movement_result = inquirer.prompt([
           inquirer.List('movement',
               message=f"Select {control_type} adjustment",
               choices=[
                   f'Large Step (±15°)',
                   f'Medium Step (±5°)',
                   f'Small Step (±1°)',
                   'Custom Value (degrees)',
                   'Back'
               ]
           )
       ])

       if not movement_result or movement_result['movement'] == 'Back':
           return

       if 'Step' in movement_result['movement']:
           self.movement_handler.handle_step_movement(
               control_type, is_pan, movement_result['movement'], 
               current_pos, self.angle_converter
           )
       else:
           self._handle_custom_movement(control_type, is_pan)

   def _handle_zoom_control(self, current_pos):
       """Handle zoom control adjustments"""
       while True:
           current_pos = self.camera.controller.get_current_position()
           console.print(f"\n[blue]Current Zoom: {current_pos['zoom']}%[/blue]")
           
           choices = [
               '🔍 Zoom In (+10%)',
               '🔍 Zoom In (+5%)',
               '🔍 Zoom Out (-5%)',
               '🔍 Zoom Out (-10%)',
               '📏 Custom Value (0-100%)',
               '↩️ Back to Control Menu'
           ]
           
           zoom_result = inquirer.prompt([
               inquirer.List('movement',
                   message=f"Select zoom adjustment (current: {current_pos['zoom']}%)",
                   choices=choices,
                   default=choices[self.last_zoom_choice]
               )
           ])

           if not zoom_result or zoom_result['movement'] == '↩️ Back to Control Menu':
               break
               
           self.last_zoom_choice = choices.index(zoom_result['movement'])

           if '📏 Custom Value' not in zoom_result['movement']:
               change = int(zoom_result['movement'].split('(')[1].split('%')[0])
               self.movement_handler.handle_zoom_adjustment(current_pos['zoom'], change)
           else:
               self._handle_custom_zoom()
               self.last_zoom_choice = 0
               
           time.sleep(0.1)

   def _handle_custom_zoom(self):
       """Handle custom zoom value input"""
       while True:
           value_result = inquirer.prompt([
               inquirer.Text('value',
                   message="Enter zoom percentage (0-100%):",
                   validate=lambda _, x: x.isdigit() and 0 <= int(x) <= 100,
                   invalid_message="Please enter a valid number between 0 and 100"
               )
           ])

           if not value_result:
               break

           try:
               zoom = int(value_result['value'])
               self.camera.controller.set_zoom(zoom)
               break
           except Exception as e:
               console.print(f"[red]Error setting zoom: {e}[/red]")
               break

   def _handle_custom_movement(self, control_type, is_pan):
       """Handle custom angle movement input"""
       while True:
           value_result = inquirer.prompt([
               inquirer.Text('value',
                   message=f"Enter {control_type} angle (-180° to +180°):"
               )
           ])

           if not value_result:
               break

           try:
               degrees = float(value_result['value'])
               if -180 <= degrees <= 180:
                   value = self.angle_converter.from_degrees(degrees, control_type)
                   if is_pan:
                       self.camera.controller.set_pan(value)
                   else:
                       self.camera.controller.set_tilt(value)
                   break
               console.print("[red]Value must be between -180° and +180°[/red]")
           except ValueError:
               console.print("[red]Please enter a valid number[/red]")