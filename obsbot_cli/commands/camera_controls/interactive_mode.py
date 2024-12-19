# commands/camera_controls/interactive_mode.py
import curses
import time
from rich.console import Console
from obsbot_cli.config.settings import CAMERA_SETTINGS
from .utils.conversion import AngleConverter

console = Console()

class InteractiveModeController:
   """🕹️ Interactive keyboard-based camera control"""
   
   def __init__(self, camera):
       self.camera = camera
       self.angle_converter = AngleConverter()
       self.PAN_STEP = 5000
       self.TILT_STEP = 5000
       self.ZOOM_STEP = 5

   def start(self):
       """Start interactive control mode"""
       try:
           curses.wrapper(self._run_interactive_control)
       except Exception as e:
           console.print(f"\n[red]Error in interactive mode: {e}[/red]")
       finally:
           console.print("\n[yellow]Exiting interactive mode...[/yellow]")

   def _run_interactive_control(self, stdscr):
       self._setup_screen(stdscr)
       self._control_loop(stdscr)

   def _setup_screen(self, stdscr):
       """Initialize the curses screen"""
       stdscr.clear()
       stdscr.nodelay(1)
       curses.curs_set(0)
       curses.start_color()
       curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
       curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
       curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

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

   def _control_loop(self, stdscr):
       """Main control loop for interactive mode"""
       while True:
           try:
               current_pos = self.camera.controller.get_current_position()
               pan_deg = self.angle_converter.to_degrees(current_pos['pan'], 'pan')
               tilt_deg = self.angle_converter.to_degrees(current_pos['tilt'], 'tilt')

               self._update_status(stdscr, pan_deg, tilt_deg, current_pos['zoom'])
               
               if not self._handle_input(stdscr, current_pos):
                   break

               time.sleep(0.05)

           except Exception as e:
               stdscr.addstr(11, 0, f"Error: {str(e)}")
               stdscr.refresh()
               time.sleep(1)
               break

   def _update_status(self, stdscr, pan_deg, tilt_deg, zoom):
       """Update status display"""
       status = f"Pan: {pan_deg:>6.1f}° | Tilt: {tilt_deg:>6.1f}° | Zoom: {zoom:>3}%"
       stdscr.addstr(9, 0, status)
       stdscr.clrtoeol()
       stdscr.refresh()

   def _handle_input(self, stdscr, current_pos):
       """Handle keyboard input"""
       key = stdscr.getch()
       if key == 27 or key == ord('q'):
           return False
       elif key == curses.KEY_LEFT:
           new_pan = max(CAMERA_SETTINGS['pan']['min'], current_pos['pan'] - self.PAN_STEP)
           self.camera.controller.set_pan(new_pan)
       elif key == curses.KEY_RIGHT:
           new_pan = min(CAMERA_SETTINGS['pan']['max'], current_pos['pan'] + self.PAN_STEP)
           self.camera.controller.set_pan(new_pan)
       elif key == curses.KEY_UP:
           new_tilt = min(CAMERA_SETTINGS['tilt']['max'], current_pos['tilt'] + self.TILT_STEP)
           self.camera.controller.set_tilt(new_tilt)
       elif key == curses.KEY_DOWN:
           new_tilt = max(CAMERA_SETTINGS['tilt']['min'], current_pos['tilt'] - self.TILT_STEP)
           self.camera.controller.set_tilt(new_tilt)
       elif key in [ord('+'), ord('=')]:
           new_zoom = min(CAMERA_SETTINGS['zoom']['max'], current_pos['zoom'] + self.ZOOM_STEP)
           self.camera.controller.set_zoom(new_zoom)
       elif key == ord('-'):
           new_zoom = max(CAMERA_SETTINGS['zoom']['min'], current_pos['zoom'] - self.ZOOM_STEP)
           self.camera.controller.set_zoom(new_zoom)
       elif key == ord('c'):
           self.camera.center()
       return True