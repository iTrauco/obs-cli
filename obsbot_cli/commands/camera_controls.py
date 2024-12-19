# import inquirer
# from rich.console import Console
# from obsbot_cli.commands.camera import CameraCommands
# from obsbot_cli.config.settings import CAMERA_SETTINGS

# console = Console()

# class CameraControlCommands:
#     """🎮 Camera manual control handler"""
    
#     def __init__(self, device):
#         self.device = device
#         self.camera = CameraCommands(device)

#     def _to_degrees(self, raw_value, control_type):
#         """Convert raw values to degrees"""
#         if control_type == "pan":
#             return round((raw_value / 468000) * 180, 1)
#         elif control_type == "tilt":
#             return round((raw_value / 324000) * 180, 1)
#         return raw_value

#     def _from_degrees(self, degrees, control_type):
#         """Convert degrees to raw values"""
#         if control_type == "pan":
#             return int((degrees / 180) * 468000)
#         elif control_type == "tilt":
#             return int((degrees / 180) * 324000)
#         return degrees

#     def handle(self):
#         """🎮 Handle camera controls menu interaction"""
#         while True:
#             current_pos = self.camera.controller.get_current_position()
#             pan_deg = self._to_degrees(current_pos['pan'], 'pan')
#             tilt_deg = self._to_degrees(current_pos['tilt'], 'tilt')
            
#             console.print(f"\n[blue]Current Position:[/blue]")
#             console.print(f"Pan: {pan_deg}° | Tilt: {tilt_deg}° | Zoom: {current_pos['zoom']}%")
            
#             questions = [
#                 inquirer.List('control',
#                     message="Select control to adjust",
#                     choices=[
#                         'Pan (Left/Right)',
#                         'Tilt (Up/Down)',
#                         'Zoom (In/Out)',
#                         'Center Camera',
#                         'Back to Main Menu'
#                     ]
#                 )
#             ]
            
#             result = inquirer.prompt(questions)
#             if not result or result['control'] == 'Back to Main Menu':
#                 break

#             if result['control'] == 'Center Camera':
#                 self.camera.center()
#                 continue

#             control = result['control'].split(' ')[0].lower()
            
#             # Show movement options based on control type
#             if control in ['pan', 'tilt']:
#                 movement_question = [
#                     inquirer.List('movement',
#                         message=f"Select {control} movement",
#                         choices=[
#                             f'Large Step ({15}°)',
#                             f'Medium Step ({5}°)',
#                             f'Small Step ({1}°)',
#                             'Custom Value (degrees)',
#                             'Back'
#                         ]
#                     )
#                 ]
                
#                 movement_result = inquirer.prompt(movement_question)
#                 if not movement_result or movement_result['movement'] == 'Back':
#                     continue
                    
#                 if 'Step' in movement_result['movement']:
#                     degrees = float(movement_result['movement'].split('(')[1].split('°')[0])
#                     direction_question = [
#                         inquirer.List('direction',
#                             message="Select direction",
#                             choices=[
#                                 f'{"Left" if control == "pan" else "Up"} ({-degrees}°)',
#                                 f'{"Right" if control == "pan" else "Down"} (+{degrees}°)',
#                                 'Back'
#                             ]
#                         )
#                     ]
                    
#                     direction_result = inquirer.prompt(direction_question)
#                     if not direction_result or direction_result['direction'] == 'Back':
#                         continue
                        
#                     degrees = degrees if '+' in direction_result['direction'] else -degrees
#                     current = self._to_degrees(current_pos[control], control)
#                     new_degrees = current + degrees
                    
#                     if -180 <= new_degrees <= 180:
#                         value = self._from_degrees(new_degrees, control)
#                         if control == 'pan':
#                             self.camera.controller.set_pan(value)
#                         else:
#                             self.camera.controller.set_tilt(value)
#                     else:
#                         console.print("[red]Movement would exceed limits[/red]")
                
#                 elif movement_result['movement'] == 'Custom Value (degrees)':
#                     value_question = [
#                         inquirer.Text('value',
#                             message=f"Enter {control} angle (-180° to +180°):"
#                         )
#                     ]
#                     value_result = inquirer.prompt(value_question)
#                     if not value_result:
#                         continue
#                     try:
#                         degrees = float(value_result['value'])
#                         if -180 <= degrees <= 180:
#                             value = self._from_degrees(degrees, control)
#                             if control == 'pan':
#                                 self.camera.controller.set_pan(value)
#                             else:
#                                 self.camera.controller.set_tilt(value)
#                         else:
#                             console.print("[red]Value must be between -180° and +180°[/red]")
#                     except ValueError:
#                         console.print("[red]Please enter a valid number[/red]")

#             elif control == 'zoom':
#                 zoom_question = [
#                     inquirer.List('movement',
#                         message="Select zoom movement",
#                         choices=[
#                             'Zoom In (+10%)',
#                             'Zoom In (+5%)',
#                             'Zoom Out (-5%)',
#                             'Zoom Out (-10%)',
#                             'Custom Value (0-100%)',
#                             'Back'
#                         ]
#                     )
#                 ]
                
#                 zoom_result = inquirer.prompt(zoom_question)
#                 if not zoom_result or zoom_result['movement'] == 'Back':
#                     continue


# obsbot_cli/commands/camera_controls.py
import inquirer
from rich.console import Console
import keyboard
import time
from obsbot_cli.commands.camera import CameraCommands 
from obsbot_cli.config.settings import CAMERA_SETTINGS

console = Console()

class CameraControlCommands:
   """🎮 Camera manual control handler"""
   
   def __init__(self, device):
       self.device = device
       self.camera = CameraCommands(device)

   def _to_degrees(self, raw_value, control_type):
       """Convert raw values to degrees"""
       if control_type == "pan":
           return round((raw_value / 468000) * 180, 1)
       elif control_type == "tilt":
           return round((raw_value / 324000) * 180, 1)
       return raw_value

   def _from_degrees(self, degrees, control_type):
       """Convert degrees to raw values"""
       if control_type == "pan":
           return int((degrees / 180) * 468000)
       elif control_type == "tilt":
           return int((degrees / 180) * 324000)
       return degrees

   def handle(self):
       """🎮 Handle camera controls menu interaction"""
       while True:
           current_pos = self.camera.controller.get_current_position()
           pan_deg = self._to_degrees(current_pos['pan'], 'pan')
           tilt_deg = self._to_degrees(current_pos['tilt'], 'tilt')
           
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
               self.interactive_control_mode()
           elif result['control'] == '📏 Precise Control (Step Values)':
               self.precise_control_mode()

   def interactive_control_mode(self):
       """🕹️ Real-time control using keyboard"""
       console.print("\n[green]🕹️ Interactive Control Mode[/green]")
       console.print("\n[yellow]Control Guide:[/yellow]")
       console.print("⬅️  ➡️  : Pan left/right")
       console.print("⬆️  ⬇️  : Tilt up/down")
       console.print("+ / - : Zoom in/out")
       console.print("C : Center camera")
       console.print("[red]ESC: Exit to menu[/red]")
       
       # Movement increments - can be adjusted for sensitivity
       PAN_STEP = 5000   # Approximately 2 degrees
       TILT_STEP = 5000  # Approximately 2 degrees
       ZOOM_STEP = 5     # 5% zoom change
       
       try:
           while True:
               if keyboard.is_pressed('esc'):
                   break
                   
               current_pos = self.camera.controller.get_current_position()
               pan_deg = self._to_degrees(current_pos['pan'], 'pan')
               tilt_deg = self._to_degrees(current_pos['tilt'], 'tilt')
               
               # Real-time position display
               print(f"\rPan: {pan_deg:>6.1f}° | Tilt: {tilt_deg:>6.1f}° | Zoom: {current_pos['zoom']:>3}%", end='')
               
               if keyboard.is_pressed('c'):
                   self.camera.center()
                   time.sleep(0.1)  # Debounce
                   
               if keyboard.is_pressed('left'):
                   new_pan = max(CAMERA_SETTINGS['pan']['min'], 
                               current_pos['pan'] - PAN_STEP)
                   self.camera.controller.set_pan(new_pan)
                   
               if keyboard.is_pressed('right'):
                   new_pan = min(CAMERA_SETTINGS['pan']['max'], 
                               current_pos['pan'] + PAN_STEP)
                   self.camera.controller.set_pan(new_pan)
                   
               if keyboard.is_pressed('up'):
                   new_tilt = min(CAMERA_SETTINGS['tilt']['max'], 
                                current_pos['tilt'] + TILT_STEP)
                   self.camera.controller.set_tilt(new_tilt)
                   
               if keyboard.is_pressed('down'):
                   new_tilt = max(CAMERA_SETTINGS['tilt']['min'], 
                                current_pos['tilt'] - TILT_STEP)
                   self.camera.controller.set_tilt(new_tilt)
                   
               if keyboard.is_pressed('+'):
                   new_zoom = min(CAMERA_SETTINGS['zoom']['max'], 
                                current_pos['zoom'] + ZOOM_STEP)
                   self.camera.controller.set_zoom(new_zoom)
                   
               if keyboard.is_pressed('-'):
                   new_zoom = max(CAMERA_SETTINGS['zoom']['min'], 
                                current_pos['zoom'] - ZOOM_STEP)
                   self.camera.controller.set_zoom(new_zoom)
                   
               time.sleep(0.05)  # Rate limiting for smooth movement
               
       except Exception as e:
           console.print(f"\n[red]Error in interactive mode: {e}[/red]")
       finally:
           console.print("\n[yellow]Exiting interactive mode...[/yellow]")

   def precise_control_mode(self):
       """📏 Precise control with step values"""
       while True:
           current_pos = self.camera.controller.get_current_position()
           pan_deg = self._to_degrees(current_pos['pan'], 'pan')
           tilt_deg = self._to_degrees(current_pos['tilt'], 'tilt')
           
           control_question = [
               inquirer.List('control',
                   message="Select control to adjust",
                   choices=[
                       '👈 Pan (Left/Right)',
                       '👆 Tilt (Up/Down)',
                       '🔍 Zoom (In/Out)',
                       '↩️ Back to Control Menu'
                   ]
               )
           ]
           
           control_result = inquirer.prompt(control_question)
           if not control_result or control_result['control'] == '↩️ Back to Control Menu':
               break

           control = control_result['control'].split(' ')[1].strip('()')

           if control in ['Left/Right', 'Up/Down']:
               is_pan = control == 'Left/Right'
               control_type = 'pan' if is_pan else 'tilt'
               
               movement_question = [
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
               ]
               
               move_result = inquirer.prompt(movement_question)
               if not move_result or move_result['movement'] == 'Back':
                   continue
                   
               if 'Step' in move_result['movement']:
                   degrees = float(move_result['movement'].split('(')[1].split('°')[0].strip('±'))
                   direction_choices = [
                       f'{"Left" if is_pan else "Up"} (-{degrees}°)',
                       f'{"Right" if is_pan else "Down"} (+{degrees}°)',
                       'Back'
                   ]
                   
                   direction_result = inquirer.prompt([
                       inquirer.List('direction',
                           message="Select direction",
                           choices=direction_choices
                       )
                   ])
                   
                   if not direction_result or direction_result['direction'] == 'Back':
                       continue
                       
                   degrees = degrees if '+' in direction_result['direction'] else -degrees
                   current = self._to_degrees(current_pos[control_type], control_type)
                   new_degrees = current + degrees
                   
                   if -180 <= new_degrees <= 180:
                       value = self._from_degrees(new_degrees, control_type)
                       if is_pan:
                           self.camera.controller.set_pan(value)
                       else:
                           self.camera.controller.set_tilt(value)
                   else:
                       console.print("[red]Movement would exceed limits[/red]")
               
               else:  # Custom Value
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
                               value = self._from_degrees(degrees, control_type)
                               if is_pan:
                                   self.camera.controller.set_pan(value)
                               else:
                                   self.camera.controller.set_tilt(value)
                               break
                           console.print("[red]Value must be between -180° and +180°[/red]")
                       except ValueError:
                           console.print("[red]Please enter a valid number[/red]")
           
           elif control == 'In/Out':
               zoom_question = [
                   inquirer.List('movement',
                       message="Select zoom adjustment",
                       choices=[
                           '🔍 Zoom In (+10%)',
                           '🔍 Zoom In (+5%)',
                           '🔍 Zoom Out (-5%)',
                           '🔍 Zoom Out (-10%)',
                           '📏 Custom Value (0-100%)',
                           '↩️ Back'
                       ]
                   )
               ]
               
               zoom_result = inquirer.prompt(zoom_question)
               if not zoom_result or zoom_result['movement'] == '↩️ Back':
                   continue
                   
               if 'Custom' not in zoom_result['movement']:
                   change = int(zoom_result['movement'].split('(')[1].split('%')[0])
                   new_zoom = current_pos['zoom'] + change
                   if 0 <= new_zoom <= 100:
                       self.camera.controller.set_zoom(new_zoom)
                   else:
                       console.print("[red]Zoom value would exceed limits[/red]")
               else:
                   while True:
                       value_result = inquirer.prompt([
                           inquirer.Text('value',
                               message="Enter zoom percentage (0-100%):"
                           )
                       ])
                       
                       if not value_result:
                           break
                           
                       try:
                           zoom = int(value_result['value'])
                           if 0 <= zoom <= 100:
                               self.camera.controller.set_zoom(zoom)
                               break
                           console.print("[red]Value must be between 0 and 100[/red]")
                       except ValueError:
                           console.print("[red]Please enter a valid number[/red]")