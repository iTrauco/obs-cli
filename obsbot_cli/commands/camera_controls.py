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
           # Clear screen and setup
           stdscr.clear()
           stdscr.nodelay(1)  # Make getch non-blocking
           curses.curs_set(0)  # Hide cursor
           curses.start_color()
           curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
           curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
           curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
           
           # Movement increments - same as before
           PAN_STEP = 5000   # Approximately 2 degrees
           TILT_STEP = 5000  # Approximately 2 degrees
           ZOOM_STEP = 5     # 5% zoom change
           
           # Print instructions with color
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
                   
                   # Update position display
                   status = f"Pan: {pan_deg:>6.1f}° | Tilt: {tilt_deg:>6.1f}° | Zoom: {current_pos['zoom']:>3}%"
                   stdscr.addstr(9, 0, status)
                   stdscr.clrtoeol()  # Clear rest of line
                   stdscr.refresh()
                   
                   # Get key input
                   key = stdscr.getch()
                   if key == 27 or key == ord('q'):  # ESC or q
                       break
                   elif key == curses.KEY_LEFT:
                       new_pan = max(CAMERA_SETTINGS['pan']['min'], 
                                   current_pos['pan'] - PAN_STEP)
                       self.camera.controller.set_pan(new_pan)
                   elif key == curses.KEY_RIGHT:
                       new_pan = min(CAMERA_SETTINGS['pan']['max'], 
                                   current_pos['pan'] + PAN_STEP)
                       self.camera.controller.set_pan(new_pan)
                   elif key == curses.KEY_UP:
                       new_tilt = min(CAMERA_SETTINGS['tilt']['max'], 
                                    current_pos['tilt'] + TILT_STEP)
                       self.camera.controller.set_tilt(new_tilt)
                   elif key == curses.KEY_DOWN:
                       new_tilt = max(CAMERA_SETTINGS['tilt']['min'], 
                                    current_pos['tilt'] - TILT_STEP)
                       self.camera.controller.set_tilt(new_tilt)
                   elif key in [ord('+'), ord('=')]:
                       new_zoom = min(CAMERA_SETTINGS['zoom']['max'], 
                                    current_pos['zoom'] + ZOOM_STEP)
                       self.camera.controller.set_zoom(new_zoom)
                   elif key == ord('-'):
                       new_zoom = max(CAMERA_SETTINGS['zoom']['min'], 
                                    current_pos['zoom'] - ZOOM_STEP)
                       self.camera.controller.set_zoom(new_zoom)
                   elif key == ord('c'):
                       self.camera.center()
                       
                   time.sleep(0.05)  # Rate limiting for smooth movement
                   
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
