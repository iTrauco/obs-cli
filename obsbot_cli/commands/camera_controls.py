import inquirer
from rich.console import Console
import curses
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
        def run_interactive_control(stdscr):
            stdscr.clear()
            stdscr.nodelay(1)
            curses.curs_set(0)
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

            PAN_STEP = 5000
            TILT_STEP = 5000
            ZOOM_STEP = 5

            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(0, 0, "🕹️ Interactive Control Mode")
            stdscr.attroff(curses.color_pair(1))

            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(2, 0, "Control Guide:")
            stdscr.addstr(3, 0, "⬅️  ➡️  : Pan left/right")
            stdscr.addstr(4, 0, "⬆️  ⬇️  : Tilt up/down")
            stdscr.addstr(5, 0, "+ / - : Zoom in/out")
            stdscr.addstr(6, 0, "c : Center camera")
            stdscr.attroff(curses.color_pair(2))

            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(7, 0, "ESC or q: Exit to menu")
            stdscr.attroff(curses.color_pair(3))

            while True:
                try:
                    current_pos = self.camera.controller.get_current_position()
                    pan_deg = self._to_degrees(current_pos['pan'], 'pan')
                    tilt_deg = self._to_degrees(current_pos['tilt'], 'tilt')

                    status = f"Pan: {pan_deg:>6.1f}° | Tilt: {tilt_deg:>6.1f}° | Zoom: {current_pos['zoom']:>3}%"
                    stdscr.addstr(9, 0, status)
                    stdscr.clrtoeol()
                    stdscr.refresh()

                    key = stdscr.getch()
                    if key == 27 or key == ord('q'):
                        break
                    elif key == curses.KEY_LEFT:
                        new_pan = max(CAMERA_SETTINGS['pan']['min'], current_pos['pan'] - PAN_STEP)
                        self.camera.controller.set_pan(new_pan)
                    elif key == curses.KEY_RIGHT:
                        new_pan = min(CAMERA_SETTINGS['pan']['max'], current_pos['pan'] + PAN_STEP)
                        self.camera.controller.set_pan(new_pan)
                    elif key == curses.KEY_UP:
                        new_tilt = min(CAMERA_SETTINGS['tilt']['max'], current_pos['tilt'] + TILT_STEP)
                        self.camera.controller.set_tilt(new_tilt)
                    elif key == curses.KEY_DOWN:
                        new_tilt = max(CAMERA_SETTINGS['tilt']['min'], current_pos['tilt'] - TILT_STEP)
                        self.camera.controller.set_tilt(new_tilt)
                    elif key in [ord('+'), ord('=')]:
                        new_zoom = min(CAMERA_SETTINGS['zoom']['max'], current_pos['zoom'] + ZOOM_STEP)
                        self.camera.controller.set_zoom(new_zoom)
                    elif key == ord('-'):
                        new_zoom = max(CAMERA_SETTINGS['zoom']['min'], current_pos['zoom'] - ZOOM_STEP)
                        self.camera.controller.set_zoom(new_zoom)
                    elif key == ord('c'):
                        self.camera.center()

                    time.sleep(0.05)

                except Exception as e:
                    stdscr.addstr(11, 0, f"Error: {str(e)}")
                    stdscr.refresh()
                    time.sleep(1)
                    break

        try:
            curses.wrapper(run_interactive_control)
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

            console.print(f"\n[blue]Current Position:[/blue]")
            console.print(f"Pan: {pan_deg}° | Tilt: {tilt_deg}° | Zoom: {current_pos['zoom']}%")

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
                break

            selected = control_result['control']
            if '👈 Pan' in selected:
                control_type = 'pan'
                is_pan = True
            elif '👆 Tilt' in selected:
                control_type = 'tilt'
                is_pan = False
            elif '🔍 Zoom' in selected:
                self.handle_zoom_control(current_pos)
                continue

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
                continue

            if 'Step' in movement_result['movement']:
                self.handle_step_movement(control_type, is_pan, movement_result['movement'], current_pos)
            else:
                self.handle_custom_movement(control_type, is_pan, current_pos)

    def handle_zoom_control(self, current_pos):
        """Handle zoom adjustments with recursive selection and preserved choice
        
        Args:
            current_pos (dict): Current camera position containing zoom value
        """
        # Track the last selected zoom option
        last_choice = 0  # Default to first option
        
        while True:  # Loop for recursive zoom adjustment
            # Get current position for updated feedback
            current_pos = self.camera.controller.get_current_position()
            
            # Show current zoom before each adjustment
            console.print(f"\n[blue]Current Zoom: {current_pos['zoom']}%[/blue]")
            
            # Create zoom choices
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
                    default=choices[last_choice]  # Set default to last selected option
                )
            ])

            if not zoom_result or zoom_result['movement'] == '↩️ Back to Control Menu':
                break
                
            # Update last_choice based on selection
            last_choice = choices.index(zoom_result['movement'])

            if '📏 Custom Value' not in zoom_result['movement']:
                # Extract zoom change value from the selected option
                change = int(zoom_result['movement'].split('(')[1].split('%')[0])
                new_zoom = current_pos['zoom'] + change
                
                # Validate zoom bounds
                if 0 <= new_zoom <= 100:
                    self.camera.controller.set_zoom(new_zoom)
                else:
                    console.print("[red]Zoom value would exceed limits (0-100%)[/red]")
            else:
                # Handle custom zoom value input
                self.handle_custom_zoom()
                # Reset last_choice after custom input to default selection
                last_choice = 0
                
            # Brief pause to allow zoom to adjust
            time.sleep(0.1)

    def handle_custom_zoom(self):
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

 
    def handle_step_movement(self, control_type, is_pan, movement, current_pos):
        """Handle step-based movement with recursive direction selection and preserved choice
        
        Args:
            control_type (str): Type of control ('pan' or 'tilt')
            is_pan (bool): Whether the control is for pan movement
            movement (str): Selected movement step size
            current_pos (dict): Current camera position
        """
        # Extract step size from movement string
        degrees = float(movement.split('(')[1].split('°')[0].strip('±'))
        
        # Track the last selected direction to preserve selection
        last_choice = 0  # Default to first option
        
        while True:  # Loop for recursive direction selection
            # Get current position for updated feedback
            current_pos = self.camera.controller.get_current_position()
            current_angle = self._to_degrees(current_pos[control_type], control_type)
            
            # Show current position before each movement
            console.print(f"\n[blue]Current {control_type}: {current_angle:>6.1f}°[/blue]")
            
            # Create direction choices
            choices = [
                f'{"Left" if is_pan else "Up"} (-{degrees}°)',
                f'{"Right" if is_pan else "Down"} (+{degrees}°)',
                'Back to Step Selection'
            ]
            
            direction_result = inquirer.prompt([
                inquirer.List('direction',
                    message=f"Select {control_type} direction (current: {current_angle:>6.1f}°)",
                    choices=choices,
                    default=choices[last_choice]  # Set default to last selected option
                )
            ])
            
            # Check for exit condition
            if not direction_result or direction_result['direction'] == 'Back to Step Selection':
                break
                
            # Update last_choice based on selection
            last_choice = choices.index(direction_result['direction'])
            
            # Calculate movement amount based on direction
            move_degrees = degrees if '+' in direction_result['direction'] else -degrees
            new_degrees = current_angle + move_degrees
            
            # Validate movement within bounds
            if -180 <= new_degrees <= 180:
                # Convert degrees to raw value and apply movement
                value = self._from_degrees(new_degrees, control_type)
                if is_pan:
                    self.camera.controller.set_pan(value)
                else:
                    self.camera.controller.set_tilt(value)
            else:
                console.print("[red]Movement would exceed limits[/red]")
                continue  # Continue loop even if movement fails
            
            # Brief pause to allow movement to complete
            time.sleep(0.1)

    def handle_custom_zoom(self):
        """Handle custom zoom value input"""
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

    def handle_custom_movement(self, control_type, is_pan, current_pos):
        """Handle custom value movement"""
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
