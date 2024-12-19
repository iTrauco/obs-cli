# # obsbot_cli/commands/camera_controls.py
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
#                 movement = inquirer.List('movement',
#                     message=f"Select {control} movement",
#                     choices=[
#                         f'Large Step ({15}°)',
#                         f'Medium Step ({5}°)',
#                         f'Small Step ({1}°)',
#                         'Custom Value (degrees)',
#                         'Back'
#                     ]
#                 ).execute()
                
#                 if movement == 'Back':
#                     continue
                    
#                 if 'Step' in movement:
#                     degrees = float(movement.split('(')[1].split('°')[0])
#                     directions = inquirer.List('direction',
#                         message="Select direction",
#                         choices=[
#                             f'{"Left" if control == "pan" else "Up"} ({-degrees}°)',
#                             f'{"Right" if control == "pan" else "Down"} (+{degrees}°)',
#                             'Back'
#                         ]
#                     ).execute()
                    
#                     if directions == 'Back':
#                         continue
                        
#                     degrees = degrees if '+' in directions else -degrees
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
                
#                 elif movement == 'Custom Value (degrees)':
#                     while True:
#                         try:
#                             value = inquirer.Text('degrees',
#                                 message=f"Enter {control} angle (-180° to +180°):"
#                             ).execute()
                            
#                             degrees = float(value)
#                             if -180 <= degrees <= 180:
#                                 value = self._from_degrees(degrees, control)
#                                 if control == 'pan':
#                                     self.camera.controller.set_pan(value)
#                                 else:
#                                     self.camera.controller.set_tilt(value)
#                                 break
#                             console.print("[red]Value must be between -180° and +180°[/red]")
#                         except ValueError:
#                             console.print("[red]Please enter a valid number[/red]")
            
#             elif control == 'zoom':
#                 movement = inquirer.List('movement',
#                     message="Select zoom movement",
#                     choices=[
#                         'Zoom In (+10%)',
#                         'Zoom In (+5%)',
#                         'Zoom Out (-5%)',
#                         'Zoom Out (-10%)',
#                         'Custom Value (0-100%)',
#                         'Back'
#                     ]
#                 ).execute()
                
#                 if movement == 'Back':
#                     continue
                    
#                 if movement != 'Custom Value (0-100%)':
#                     change = int(movement.split('(')[1].split('%')[0])
#                     new_zoom = current_pos['zoom'] + change
#                     if 0 <= new_zoom <= 100:
#                         self.camera.controller.set_zoom(new_zoom)
#                     else:
#                         console.print("[red]Zoom value would exceed limits[/red]")
#                 else:
#                     while True:
#                         try:
#                             value = inquirer.Text('zoom',
#                                 message="Enter zoom percentage (0-100%):"
#                             ).execute()
                            
#                             zoom = int(value)
#                             if 0 <= zoom <= 100:
#                                 self.camera.controller.set_zoom(zoom)
#                                 break
#                             console.print("[red]Value must be between 0 and 100[/red]")
#                         except ValueError:
#                             console.print("[red]Please enter a valid number[/red]")





import inquirer
from rich.console import Console
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
            
            console.print(f"\n[blue]Current Position:[/blue]")
            console.print(f"Pan: {pan_deg}° | Tilt: {tilt_deg}° | Zoom: {current_pos['zoom']}%")
            
            questions = [
                inquirer.List('control',
                    message="Select control to adjust",
                    choices=[
                        'Pan (Left/Right)',
                        'Tilt (Up/Down)',
                        'Zoom (In/Out)',
                        'Center Camera',
                        'Back to Main Menu'
                    ]
                )
            ]
            
            result = inquirer.prompt(questions)
            if not result or result['control'] == 'Back to Main Menu':
                break

            if result['control'] == 'Center Camera':
                self.camera.center()
                continue

            control = result['control'].split(' ')[0].lower()
            
            # Show movement options based on control type
            if control in ['pan', 'tilt']:
                movement_question = [
                    inquirer.List('movement',
                        message=f"Select {control} movement",
                        choices=[
                            f'Large Step ({15}°)',
                            f'Medium Step ({5}°)',
                            f'Small Step ({1}°)',
                            'Custom Value (degrees)',
                            'Back'
                        ]
                    )
                ]
                
                movement_result = inquirer.prompt(movement_question)
                if not movement_result or movement_result['movement'] == 'Back':
                    continue
                    
                if 'Step' in movement_result['movement']:
                    degrees = float(movement_result['movement'].split('(')[1].split('°')[0])
                    direction_question = [
                        inquirer.List('direction',
                            message="Select direction",
                            choices=[
                                f'{"Left" if control == "pan" else "Up"} ({-degrees}°)',
                                f'{"Right" if control == "pan" else "Down"} (+{degrees}°)',
                                'Back'
                            ]
                        )
                    ]
                    
                    direction_result = inquirer.prompt(direction_question)
                    if not direction_result or direction_result['direction'] == 'Back':
                        continue
                        
                    degrees = degrees if '+' in direction_result['direction'] else -degrees
                    current = self._to_degrees(current_pos[control], control)
                    new_degrees = current + degrees
                    
                    if -180 <= new_degrees <= 180:
                        value = self._from_degrees(new_degrees, control)
                        if control == 'pan':
                            self.camera.controller.set_pan(value)
                        else:
                            self.camera.controller.set_tilt(value)
                    else:
                        console.print("[red]Movement would exceed limits[/red]")
                
                elif movement_result['movement'] == 'Custom Value (degrees)':
                    value_question = [
                        inquirer.Text('value',
                            message=f"Enter {control} angle (-180° to +180°):"
                        )
                    ]
                    value_result = inquirer.prompt(value_question)
                    if not value_result:
                        continue
                    try:
                        degrees = float(value_result['value'])
                        if -180 <= degrees <= 180:
                            value = self._from_degrees(degrees, control)
                            if control == 'pan':
                                self.camera.controller.set_pan(value)
                            else:
                                self.camera.controller.set_tilt(value)
                        else:
                            console.print("[red]Value must be between -180° and +180°[/red]")
                    except ValueError:
                        console.print("[red]Please enter a valid number[/red]")

            elif control == 'zoom':
                zoom_question = [
                    inquirer.List('movement',
                        message="Select zoom movement",
                        choices=[
                            'Zoom In (+10%)',
                            'Zoom In (+5%)',
                            'Zoom Out (-5%)',
                            'Zoom Out (-10%)',
                            'Custom Value (0-100%)',
                            'Back'
                        ]
                    )
                ]
                
                zoom_result = inquirer.prompt(zoom_question)
                if not zoom_result or zoom_result['movement'] == 'Back':
                    continue
