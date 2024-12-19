# obsbot_cli/utils/camera.py
import subprocess
import json
from pathlib import Path
from rich.console import Console

console = Console()

class CameraManager:
    """🎥 Camera device management and discovery utilities"""
    
    @staticmethod
    def list_obsbot_devices():
        """📝 List all OBSBOT camera devices"""
        try:
            cmd = ['v4l2-ctl', '--list-devices']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            devices = []
            current_device = None
            
            for line in result.stdout.splitlines():
                if 'OBSBOT' in line:
                    current_device = {
                        'name': line.strip().split(':')[0],
                        'devices': []
                    }
                elif current_device and '/dev/video' in line:
                    current_device['devices'].append(line.strip())
                elif current_device:
                    devices.append(current_device)
                    current_device = None
                    
            if current_device:
                devices.append(current_device)
                
            return devices
        except subprocess.CalledProcessError as e:
            console.print("[red]Error listing devices:[/red]", e.stderr)
            return []

    @staticmethod
    def verify_device(device_path):
        """✅ Verify if device exists and is accessible"""
        try:
            cmd = ['v4l2-ctl', '-d', device_path, '--all']
            subprocess.run(cmd, capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def get_device_capabilities(device_path):
        """💡 Get device capabilities and supported controls"""
        try:
            # Get controls
            cmd = ['v4l2-ctl', '-d', device_path, '--list-ctrls']
            controls = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Get formats
            cmd = ['v4l2-ctl', '-d', device_path, '--list-formats-ext']
            formats = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            return {
                'controls': controls.stdout,
                'formats': formats.stdout
            }
        except subprocess.CalledProcessError as e:
            console.print("[red]Error getting device capabilities:[/red]", e.stderr)
            return None

    @staticmethod
    def setup_device_permissions(device_path):
        """🔐 Set up proper device permissions"""
        try:
            # Make device readable/writable
            subprocess.run(['sudo', 'chmod', '666', device_path], check=True)
            console.print(f"[green]Set permissions for {device_path}[/green]")
            return True
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error setting permissions: {e}[/red]")
            return False