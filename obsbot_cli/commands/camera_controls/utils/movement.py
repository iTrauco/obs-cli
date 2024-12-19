# # commands/camera_controls/utils/movement.py
# from rich.console import Console
# import time
# import inquirer

# console = Console()

# class MovementHandler:
#    """Handle camera movement operations"""
   
#    def __init__(self, camera):
#        self.camera = camera

#    def handle_step_movement(self, control_type, is_pan, movement, current_pos, angle_converter):
#        """Handle step-based movement with recursive direction selection and preserved choice
       
#        Args:
#            control_type (str): Type of control ('pan' or 'tilt')
#            is_pan (bool): Whether the control is for pan movement
#            movement (str): Selected movement step size
#            current_pos (dict): Current camera position
#            angle_converter: Converter for angle calculations
#        """
#        # Extract step size from movement string
#        degrees = float(movement.split('(')[1].split('°')[0].strip('±'))
       
#        # Track the last selected direction to preserve selection
#        last_choice = 0  # Default to first option
       
#        while True:  # Loop for recursive direction selection
#            # Get current position for updated feedback
#            current_pos = self.camera.controller.get_current_position()
#            current_angle = angle_converter.to_degrees(current_pos[control_type], control_type)
           
#            # Show current position before each movement
#            console.print(f"\n[blue]Current {control_type}: {current_angle:>6.1f}°[/blue]")
           
#            if not self._process_direction_choice(control_type, is_pan, degrees, current_angle, last_choice, angle_converter):
#                break
           
#            # Brief pause to allow movement to complete
#            time.sleep(0.1)

#    def apply_movement(self, control_type, value, is_pan):
#        """Apply movement to specified control"""
#        if is_pan:
#            return self.camera.controller.set_pan(value)
#        else:
#            return self.camera.controller.set_tilt(value)

#    def handle_zoom_adjustment(self, current_zoom, change):
#        """Handle zoom value adjustment"""
#        new_zoom = current_zoom + change
#        if 0 <= new_zoom <= 100:
#            return self.camera.controller.set_zoom(new_zoom)
#        console.print("[red]Zoom value would exceed limits (0-100%)[/red]")
#        return False

#    def _process_direction_choice(self, control_type, is_pan, degrees, current_angle, last_choice, angle_converter):
#        """Process direction choice for movement"""
#        choices = [
#            f'{"Left" if is_pan else "Up"} (-{degrees}°)',
#            f'{"Right" if is_pan else "Down"} (+{degrees}°)',
#            'Back to Step Selection'
#        ]
       
#        direction_result = self._get_direction_input(control_type, current_angle, choices, last_choice)
#        if not direction_result or direction_result['direction'] == 'Back to Step Selection':
#            return False
           
#        # Calculate and apply movement
#        move_degrees = degrees if '+' in direction_result['direction'] else -degrees
#        new_degrees = current_angle + move_degrees
       
#        if -180 <= new_degrees <= 180:
#            value = angle_converter.from_degrees(new_degrees, control_type)
#            self.apply_movement(control_type, value, is_pan)
#        else:
#            console.print("[red]Movement would exceed limits[/red]")
           
#        return True

#    def _get_direction_input(self, control_type, current_angle, choices, last_choice):
#        """Get direction input from user"""
#        from inquirer import List, prompt
#        return prompt([
#            List('direction',
#                message=f"Select {control_type} direction (current: {current_angle:>6.1f}°)",
#                choices=choices,
#                default=choices[last_choice]
#            )
#        ])




# commands/camera_controls/utils/movement.py
from rich.console import Console
import inquirer
import time

console = Console()

class MovementHandler:
    """Handle camera movement operations"""
    
    def __init__(self, camera):
        self.camera = camera
        self.last_direction_choice = {}  # Store last choice per control type

    def handle_step_movement(self, control_type, is_pan, movement, current_pos, angle_converter):
        """Handle step-based movement with recursive direction selection and preserved choice
        
        Args:
            control_type (str): Type of control ('pan' or 'tilt')
            is_pan (bool): Whether the control is for pan movement
            movement (str): Selected movement step size
            current_pos (dict): Current camera position
            angle_converter: Converter for angle calculations
        """
        # Extract step size from movement string
        degrees = float(movement.split('(')[1].split('°')[0].strip('±'))
        
        # Initialize last choice for this control type if not exists
        if control_type not in self.last_direction_choice:
            self.last_direction_choice[control_type] = 0
        
        while True:  # Loop for recursive direction selection
            # Get current position for updated feedback
            current_pos = self.camera.controller.get_current_position()
            current_angle = angle_converter.to_degrees(current_pos[control_type], control_type)
            
            # Show current position before each movement
            console.print(f"\n[blue]Current {control_type}: {current_angle:>6.1f}°[/blue]")
            
            if not self._process_direction_choice(control_type, is_pan, degrees, current_angle, angle_converter):
                break
            
            # Brief pause to allow movement to complete
            time.sleep(0.1)

    def _process_direction_choice(self, control_type, is_pan, degrees, current_angle, angle_converter):
        """Process direction choice for movement"""
        choices = [
            f'{"Left" if is_pan else "Up"} (-{degrees}°)',
            f'{"Right" if is_pan else "Down"} (+{degrees}°)',
            'Back to Step Selection'
        ]
        
        direction_result = self._get_direction_input(control_type, current_angle, choices)
        if not direction_result or direction_result['direction'] == 'Back to Step Selection':
            return False
            
        # Update last choice
        self.last_direction_choice[control_type] = choices.index(direction_result['direction'])
        
        # Calculate movement (inverting the sign for tilt to fix up/down direction)
        move_degrees = degrees if '+' in direction_result['direction'] else -degrees
        if not is_pan:  # Invert tilt direction
            move_degrees = -move_degrees
            
        new_degrees = current_angle + move_degrees
        
        if -180 <= new_degrees <= 180:
            value = angle_converter.from_degrees(new_degrees, control_type)
            self.apply_movement(control_type, value, is_pan)
        else:
            console.print("[red]Movement would exceed limits[/red]")
            
        return True

    def _get_direction_input(self, control_type, current_angle, choices):
        """Get direction input from user"""
        return inquirer.prompt([
            inquirer.List('direction',
                message=f"Select {control_type} direction (current: {current_angle:>6.1f}°)",
                choices=choices,
                default=choices[self.last_direction_choice.get(control_type, 0)]  # Use stored choice
            )
        ])

    def apply_movement(self, control_type, value, is_pan):
        """Apply movement to specified control"""
        if is_pan:
            return self.camera.controller.set_pan(value)
        else:
            return self.camera.controller.set_tilt(value)

    def handle_zoom_adjustment(self, current_zoom, change):
        """Handle zoom value adjustment"""
        new_zoom = current_zoom + change
        if 0 <= new_zoom <= 100:
            return self.camera.controller.set_zoom(new_zoom)
        console.print("[red]Zoom value would exceed limits (0-100%)[/red]")
        return False
